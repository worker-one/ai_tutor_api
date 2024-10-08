## Предложение

Я предлагаю разработку в два этапа, на втором этапе реализуются наиболее сложные элементы и элементы, которые требуют уточнения. Между этапами происходит тестирование на протяжении неопределенного времени.

## Этап 1: 

Заказчик предоставляет ключ OPENAI, исполнитель предоставляет сервер для тестирования бота.

Цель: Создать телеграм бот предназначенный для решения различного рода математических формул, уравнений, задач на основе изображения, которое присылает пользователь. 

- тг бот
- подключение к chatgpt
- два режима: пошаговое решение, короткий ответ
- в пошаговом решении пользователь получает ссылку на html страницу с ответом бота, последующие сообщения к ответу боту игнорируются.
- в коротком ответе пользователь получает только ответ, например, `x = 5`, последующие сообщения к ответу боту игнорируются.
- если пользователь отправляет сообщение, которое не содержит задачу, то бот должен сообщить о некорректности задачи.
- при отправки сообщения бот сообщает о получении запроса.
- полноценное меню из 4 кнопок:
  - Short explanation
  - Step-by-step explanation
  - Billing (фиктивная)
  - Feedback (фиктивная)
- БЕЗ тарифов и экваринга
- БЕЗ обратной связи

Срок: 5-7 дней, цена 15000 руб

## Этап 2:

На данном этапе расширяется функционал обработки входных данных пользователя, добавляется мультиязыковая поддержка, а так же фукционал для аналитики действий пользователей. Кроме того, добавляется обработка ряда исключительных ситуаций, при который пользователю сообщается об ошибке. Например, если текст пользователя слишком короткий (1-2 символа), то мы сможем отлавливать такие тексты перед отправкой на сервис openai и экономить на токенах.

- Поддержка двух языков: английский и русский. Выбор языка осуществляется через кнопку главного меню.
- В случае отправки изображения пользователь сможет добавить текст в качестве пояснения.
- Кнопка меню слева от поля ввода сообщения.
- Обратная связь. Пользователь будет иметь возможность поставить оценку боту (от 1 до 5) и опционально написать текст обратной связи через нажатие соответствующей кнопки главного меню, данная инфомарция будет сохранена в базу данных в таблицу Feedback.
- База данных со следующими таблицами:
   - `User` (id, username, language, signup_timestamp) - все пользователи, которые написали боту хотя бы одно сообщение
   - `Message` (user_id, timestamp, content) - сообщение отправленное пользователем боту
   - `Feedback` (username, timestamp, rating, comment) - запись обратной связи пользователя (оценка и комментарий), отправленная через кнопку обратной связи.
- Кабинет админа бота (доступ через команду `/admin` и пароль), который позволяет выполнять различные административные задачи:
   - Выгрузка таблица баз данных за заданный период времени.
   - Другое ?
- Обработка исключительных ситуаций:
  - текст пользователя слишком короткий.
  - текст пользователя слишком длинный.
  - изображение пользователя слишком большое.
  - неподдерживаемый формат файла пользователя (т.е. все кроме png, jpg).
  - пользователь задает follow-up вопрос или уточнение (будет доступно только в режиме AI наставника).
 
Срок: 14 дней, цена 10000р

## Этап 3 (черновик):

- тарифный план
- AI наставник = бот дает рекомендации по решению задачи, не давая полноценное решение, а лишь направляя ход мысли.
- Все веб страницы со сгенерированным ответом сохраняются и остаются активными на протяжении N месяцев.

Срок: 4-10 дней, цена 8000 - 15000 руб

## Ссылки

[1]
