# Title
Этот проект был написанн для динамической выгрузки Email сообщений из различных почтовых ящиков.
Реализация на основе WebSocket

# To Do
## Для выполенения данной задачи были реализованны классы:
1. AbstractConnection - Абстрактный класс определяющий каркас.
2. BaseConnection - Общий класс выполняющий базовые потребности, неоходим для паттерна "стратегия".

3. GmailConnection - Специализированный класс для подключения Gmail почты.
4. YandexConnection - Специализированный класс для подключения Yandex почты.
5. MailConnection - Специализированный класс для подключения Mail почты.

Данные классы так же могут проверять подключение на уровне валидации, тем самым
проверяется достоверность почты.
Для данной проверки нужно указать дополнительный аргумент form который является окружением формы.

```Python
GmailConnection.connection(
                    login=address,
                    password=password,
                    form=form,
                )
```

Для подкючения и получения списка всех писем из ящика:
```Python
server = GmailConnection
connection = server(email.address,
                    email.password,
                    limit=email.last_index,
                    )
```
В данном случае важно указать limit, так как это последнее зафиксированное Email сообщение
которое обработала программа.

Реализованны каркасные методы (магические).
```Python
len(connection) # Длина списка писем
connection[index] # Получить любое письмо по индексу
connection.reverse() # Список в обратном порядке
for item in connection: # Итеррация по списку
with connection as list_: # Менеджер открывает список писем
```

Для дальнейшей обработки списка нужен парсер.
Реализован класс:
1. Parser.
2. TextParser.
3. FileParser.

Класс Parser автоматически вмещает в себе остальные классы для обработки.
Для работы Parser, ему необходим только экземпляр Соединения IMAP4_SSL, а так же uid (ID сообщения)
```Python
parser = Parser(connection.server, uid)
message = parser.parse()
```
Это все что необходимо для выполнения работы Parser.
Parser отдает dict со всеми данными что получилось изьять из сообщения.

# WebSocket
## Для реализации WebSocket нужно:
1. Инициализировать экземпляр WebSocket на языке JavaSctipt
```JavaScript
const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/email/download/'
        + pk
        + '/'
    );
```
2. Определить действия для каждого события
```JavaScript
socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
};
socket.onopen = function(e) {
    // some move
};
socket.onclose = function(e) {
    this.close()
    console.log('Socket closed unexpectedly');
};
```
3. Написать потребителя AsyncWebsocketConsumer
4. Указать Routing
5. Изменить точку входа на asgi с помощью ProtocolTypeRouter с указанием websocket
```Python
application = ProtocolTypeRouter(dict(
    http=django_asgi_app,
    websocket=AuthMiddlewareStack(
        URLRouter(
            mailscaner.routing.websocket_urlpatterns
        )
    ),
))
```
# Dependencies
## Зависимости необходимые проекту:
1. Django
2. daphne
3. channels
4. channels-redis
5. redis
6. psycopg2-binary
7. python-dotenv
8. pillow
9. bs4

Все зависимости прописаны в pyproject.toml

# Install
## Для успешной установки следующие инструкции:
В проекте присутствует Docker. Если у вас нет Docker вы можете установить его через официальный сайт.
1. Настройте ".env.sample" и переменуйте файл в ".env"
```shell
TEST_EMAIL_HOST_GMAIL=email # Тестовая почта
TEST_EMAIL_PASSWORD_GMAIL=password # Пароль от почты

POSTGRES_PASSWORD=password # Пароль от базы данных на уровне настройки
DB_PASSWORD=password # Пароль от базы данных на уровне использования
```
Данные строки нужно заполнить
2. Сделайте билд образов.
```bash
docker compose build
```
3. Запустите контейнеры
```bash
docker compose up
```

# Using
Для перехода на сайт перейдите по адресу:
http://localhost:8000/
- Вы попадете на страницу аутентификации.
- В первую очередь вам нужно зарегистрироваться (Registration).
- Вводите данные в форму и регистрируете пользователя.
- Затем аутентифицируетесь.
- Вы видите 3 объекта Gmail, Yandex, Mail.ru, но для начало вам нужно зарегистрировать почту.
- Нажимаете Add Email.
- Вводите Email и Password, система автоматически определит что Email из разшенных и проверит достоверность введенных данных.
!!! Внимание! Обычные пароли от почты не подходят, вам нужно зайти на ваш почтовый ящик и разрешить IMAP соединения,
а так же сгенерировать пароль для приложения. Этот пароль вам пригодится для регистрации почты. !!!
- После регистрации почты переходите на соотвествующий пункт, например Gmail и у вас будет список Эмеилов этой категории.
- Нажимаете UploadData.
- Вы попадаете на страницу загрузки - начинается загрузка сообщений.
- Вы можете вернуться обратно и нажать Show list, где уже будут загруженные сообщения.
!!! Внимание! При выходе из страницы загрузки - загрузка прекращается, но сохраняется последняя точка. !!!
- По нажатию на любое из сообщений откроется его полный вид со всеми данными.
- По наличию вложенных файлов на данной странице возможно их просмотреть.

# Tests
## В данном проекте всего 2 теста.
- Для проведения теста удостоверьтесь что вы указали соотвествующие поля в ".env"
- Для теста вам нужно зайти в docker контейнер приложения.
```bash
docker ps
```
- Найдите контейнер с названием config
- Выделите его id (Хватит первых 2-3 символов)
- Запустите контейнер в интерактивном режиме
```bash
docker exec -it id_number bash
```
- Вы попадете в внутрь контейнера в оболочке bash (Если ошибка можете попробовать "bin/bash")
- Введите команду.
```bash
python manage.py test
```
- У вас будут проведенны тесты.