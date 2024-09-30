import logging
from datetime import datetime

from fastapi import APIRouter, File, UploadFile, Form
from hydra.utils import instantiate
from ai_tutor_api.api.schemas import ModelConfig, QueryModelRequest, QueryModelResponse
from ai_tutor_api.core.llm import LLM
from ai_tutor_api.db import crud
from ai_tutor_api.utils.exceptions import ChatDoesNotExist, MessageIsEmpty, MessageIsTooLong, UserDoesNotExist
from omegaconf import OmegaConf
from PIL import Image
import io

# Load logging configuration with OmegaConf
logging_config = OmegaConf.to_container(OmegaConf.load("./src/ai_tutor_api/conf/logging_config.yaml"), resolve=True)
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

config = OmegaConf.load("./src/ai_tutor_api/conf/config.yaml")
model_config = instantiate(config.llm.config.default)
llm = LLM(model_config)

logger.info(f"Model configuration: {model_config}")

router = APIRouter()

MAX_MESSAGE_LENGTH = 2000

@router.get("/model/config")
def get_model_config() -> ModelConfig:
    return llm.config

@router.post("/model/config")
def update_model_config(request: ModelConfig):
    global llm
    try:
        llm.update_config(request)
        return {"status": "success", "message": "Model updated successfully"}
    except Exception as e:
        logger.error(f"Error updating model: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/model/query")
async def query(
    user_id: str = Form(...),
    chat_id: str = Form(...),
    user_message: str = Form(None),
    config: ModelConfig = Form(None),
    file: UploadFile = File(None)  # Accept file uploads for images
) -> QueryModelResponse:
    # check if user exists
    db_user = crud.read_user(user_id)
    if db_user is None:
        raise UserDoesNotExist()

    # check if chat exists
    db_chat = crud.get_chat(chat_id, user_id)
    if db_chat is None:
        raise ChatDoesNotExist()

    if not user_message and file is None:
        raise MessageIsEmpty()

    if user_message and len(user_message) > MAX_MESSAGE_LENGTH:
        raise MessageIsTooLong()

    logger.info(f"User {user_id} sent message: `{user_message}` in chat {chat_id}")

    # add the message to the chat history if it exists
    if user_message:
        crud.create_message(chat_id, "user", content=user_message, timestamp=datetime.now())

    # get the chat history
    chat_history = crud.get_chat_history(chat_id)

    # Process the image if uploaded
    image = None
    if file:
        try:
            image_bytes = await file.read()  # Read the file contents
            image = Image.open(io.BytesIO(image_bytes))  # Convert to PIL Image
            logger.info(f"Received image from user {user_id}")
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise e

    # invoke the model with chat history and optionally with the image
    try:
        response = llm.invoke(chat_history, config, image=image)
        ai_message = response.response_content
    except Exception as e:
        logger.error(f"Error invoking model: {e}")
        raise e

    logger.info(f"AI responded with message: `{ai_message}`")

    try:
        # add the response to the chat history
        crud.create_message(chat_id, "assistant", content=ai_message, timestamp=datetime.now())
    except Exception as e:
        logger.error(f"Error adding AI message to chat history: {e}")
        raise e

    response = QueryModelResponse(
        user_id=user_id,
        chat_id=chat_id,
        model_response=response
    )
    return response
