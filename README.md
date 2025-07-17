
# Проект "Веб-приложение рассылки с помощью Django"

## Содержание:
- [Описание](#описание)
- [Проверить версию Python](#проверить-версию-python)
- [Установка Poetry](#установка-poetry)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Кастомные команды](#кастомные-команды)
- [Структура проекта](#структура-проекта)
- [Приложение client_connect](#приложение-client_connect)
  - [Admin client_connect](#admin-client_connect)
    - [RecipientAdmin](#recipientadmin)
    - [MessageAdmin](#messageadmin)
    - [MailingAdmin](#mailingadmin)
    - [SendingAttemptAdmin](#sendingattemptadmin)
  - [Forms client_connect](#forms-client_connect)
    - [RecipientForm](#recipientform)
    - [MessageForm](#messageform)
    - [MailingForm](#mailingform)
  - [Services users](#services-client_connect)
    - [AccessControlService](#accesscontrolservice)
    - [MailingService](#mailingservice)
  - [Models client_connect](#models-client_connect)
    - [Model_Recipient](#model_recipient)
    - [Model_Message](#model_message)
    - [Model_Mailing](#model_mailing)
    - [Model_SendingAttempt](#model_sendingattempt)
  - [Urls client_connect](#urls-client_connect)
  - [Views client_connect](#views-client_connect)
    - [BaseLoginView](#baseloginview)
    - [RecipientsListViews](#recipientslistviews)
    - [MessagesListView](#messageslistview)
    - [MailingsListView](#mailingslistview)
    - [RecipientCreateView](#recipientcreateview)
    - [RecipientDetailView](#recipientdetailview)
    - [RecipientUpdateView](#recipientupdateview)
    - [RecipientDeleteView](#recipientdeleteview)
    - [MessageCreateView](#messagecreateview)
    - [MessageDetailView](#messagedetailview)
    - [MessageUpdateView](#messageupdateview)
    - [MessageDeleteView](#messagedeleteview)
    - [MailingCreateView](#mailingcreateview)
    - [MailingDetailView](#mailingdetailview)
    - [MailingUpdateView](#mailingupdateview)
    - [MailingDeleteView](#mailingdeleteview)
    - [SendingAttemptsListView](#sendingattemptslistview)
- [Приложение users](#приложение-users)
  - [Admin users](#admin-users)
    - [CustomUserAdmin](#customuseradmin)
  - [Forms users](#forms-users)
    - [CustomUserCreationForm](#customusercreationform)
    - [UserUpdateForm](#userupdateform)
    - [CustomAuthenticationForm](#customauthenticationform)
    - [PasswordRecoveryForm](#passwordrecoveryform)
    - [NewPasswordForm](#newpasswordform)
  - [Models user](#models-users)
    - [CustomUser](#customuser)
  - [Services users](#services-users)
    - [CustomUserService](#customuserservice)
  - [Urls users](#urls-users)
  - [Views users](#views-users)
    - [RegisterView](#registerview)
    - [UserActivationView](#useractivationview)
    - [CustomLoginView](#customloginview)
    - [PasswordRecoveryView](#passwordrecoveryview)
    - [NewPassword](#newpassword)
    - [UsersListView](#userslistview)
    - [ActivationUserView](#activationuserview)
    - [DeactivateUserView](#deactivateuserview)

   
## Описание:

Разработка приложения(веб-сайта) с рассылкой сообщений, с помощью фреймворка Django.

[<- на начало](#содержание)


## Проверить версию Python:

Убедитесь, что у вас установлен Python (версия 3.x). Вы можете проверить установленную версию Python, выполнив команду:
```
python --version
```

[<- на начало](#содержание)


## Установка Poetry:
Если у вас еще не установлен Poetry, вы можете установить его, выполнив следующую команду
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Проверить Poetry добавлен в ваш PATH.
```bash
poetry --version
```

[<- на начало](#содержание)


## Установка:
- Клонируйте репозиторий:
```bash
git clone git@github.com:Streiker-Saik/CourseProject_4.git
```
- Перейдите в директорию проекта:
```
cd CourseProject_4
```
### При использовании PIP:
- Активируйте виртуальное окружение
```
python -m venv <имя_вашего окружения>
<имя_вашего_окружения>\Scripts\activate
```
- Установите зависимости
```
pip install -r requirements.txt
```
### При использование POETRY:
- Активируйте виртуальное окружение
```bash
poetry shell
```
- Установите необходимые зависимости:
```bash
poetry install
```
или
```bash
poetry add django python-dotenv psycopg2 redis pillow
poetry add --group lint flake8 black isort mypy ipython
```
- Зайдите в файл .env.example и следуйте инструкция

[<- на начало](#содержание)


## Запуск проекта:
Чтобы запустить сервер разработки, выполните следующую команду:
```bash
python manage.py runserver
```
! Если включено кэширования(обязательно запустить сервер redis)
```bash
redis-server
```

[<- на начало](#содержание)

---
## Кастомные команды
### add_groups
Команда для добавления групп из fixture
- 'group_fixture.json'
```bash
python manage.py add_groups
```
### add_test_data
Команда для добавления тестовых данных(получатели, сообщения, рассылки) из fixture
- 'recipient_fixture.json'
- 'message_fixture.json'
- 'mailing_fixture.json'
```bash
python manage.py add_test_data
```

[<- на начало](#содержание)

---
## Структура проекта:
```
OnlineStore_Django/
├── client_connect/ # приложение блог
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   ├── ...
|   |   └── __init__.py
|   ├── templates/ # шаблоны html
|   |   └── client_connect/
|   |   |   └── mailing/
|   |   |   |   ├── mailing_list.html
|   |   |   |   ├── mailing_confirm_delete.html
|   |   |   |   ├── mailing_detail.html
|   |   |   |   └── mailing_form.html
|   |   |   └── message/
|   |   |   |   ├── message_list.html
|   |   |   |   ├── message_confirm_delete.html
|   |   |   |   ├── message_detail.html
|   |   |   |   └── message_form.html
|   |   |   └── recipient/
|   |   |   |   ├── recipient_list.html
|   |   |   |   ├── recipient_confirm_delete.html
|   |   |   |   ├── recipient_detail.html
|   |   |   |   └── recipient_form.html
|   |   |   └── sending_attempt/
|   |   |   |   └── sending_attempts_list.html
|   |   |   ├── base.html # базовый шаблон
|   |   |   └── header.html # верхняя часть страницы(меню)
|   ├── __init__.py
|   ├── admin.py # регистрация моделе в админке
|   ├── apps.py
|   ├── forms.py # шаблоны форм
|   ├── models.py # модели БД
|   ├── services.py # сервис
|   ├── tests.py 
|   └── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── config/
|   ├── __init__.py
|   ├── asgi.py
|   ├── settings.py
|   ├── urls.py # маршрутизация проета
|   └── wsgi.py
├── static/
|   ├── css/
|   |   └── ...
|   └── js/
|   |   └── ...
├── users/ # приложение аутефикации
|   ├── fixture/ # фикстуры
|   |   └── ...
|   ├── migrations/ # пакет миграции моделей
|   |   ├── 0001_initial.py
|   |   ├── ...
|   |   └── __init__.py
|   ├── templates/ # шаблоны html
|   |   └── users/
|   |   |   ├── login.html # шаблон авторизации
|   |   |   ├── new_password.html # шаблон 
|   |   |   ├── password_reset_complete.html # шаблон успешного изменения пароля
|   |   |   ├── password_reset_confirm.html # шаблон изменения пароля
|   |   |   ├── password_reset_done.html # шаблон успешной отработки формы востановления пароля 
|   |   |   ├── password_reset_form.html # шаблон формы востановления пароля
|   |   |   ├── register.html # шаблон регистрации редоктирования
|   |   |   ├── user_detail.html # шаблон информации о пользователе
|   |   |   └── user_list.html # шаблон списка пользователей
|   ├── templatetages/ 
|   |   └── my_tags.py
|   ├── admin.py 
|   ├── apps.py
|   ├── forms.py # формы
|   ├── models.py # модели БД
|   ├── tests.py 
|   └── urls.py # маршрутизация приложения
|   └── views.py # конструктор контроллеров
├── .env
├── .flake8 # настройка для flake8
├── .gitignore
├── manage.py
├── poetry.lock
├── pypproject.toml # зависимости для poetry
├── README.md
└── requirements.txt # ависимости для pip
```

[<- на начало](#содержание)

---
# Приложение client_connect:

## Admin client_connect

### RecipientAdmin
Представление для работы администратора для управления получателями
- Вывод на дисплей: **id**, **email**(эл.почта), **full_name**(ФИО) и **comment**(комментарий)
- Поиск по **email**(эл.почта)
### MessageAdmin
Представление для работы администратора для управления сообщениями
- Вывод на дисплей: **id**, **subject**(заголовок) и **body**(содержание)
- Поиск по **subject**(заголовок) и **body**(содержание)
### MailingAdmin
Представление для работы администратора для управления рассылкой
- Вывод на дисплей: **id**, **start_time**(дата начала), **end_time**(дата окончания), **status**(статус) и 
**message**(сообщение)
- Фильтрация по **status**(статус)
- Сортировка по **update_at**(дата окончания)
### SendingAttemptAdmin
Представление для работы администратора для управления попыткой рассылки
- Вывод на дисплей: **id**, **created_at**(дата создания), **status**(статус), **answer**(ответ почтового сервера) и 
**mailing**(рассылка)
- Фильтрация по **status**(статус)
- Сортировка по **created_at**(дата и время создания)

[<- на начало](#содержание)

---
## Forms client_connect:

### RecipientForm
Форма для создания и редактирования получателя.
Исключает поле владелец(owner)
Методы __init__(self, *args, **kwargs) -> None:
  Инициализация стилизации форм:
  - стилизация полей: email, full_name, comment

### MessageForm
Форма для создания и редактирования сообщений.
Исключает поле владелец(owner)
Методы __init__(self, *args, **kwargs) -> None:
  Инициализация стилизации форм:
  - стилизация полей: subject, body

### MailingForm
Форма для создания и редактирования рассылки.
Включает поля: сообщение(message), получатели(recipients)
Методы __init__(self, *args, **kwargs) -> None:
  Инициализация стилизации форм:
  - стилизация полей: message, recipient

[<- на начало](#содержание)

---
## Models client_connect:
- **Recipient**: Представление получателя
- **Message**: Представление сообщения
- **Mailing**: Представление рассылки
- **SendingAttempt**: Представление попытки рассылки

### Model_Recipient:
- **email**: Электронная почта, уникальная
- **full_name**: Ф.И.О., ограничение 150 символами
- **comment**: Комментарий, без ограничений
- **owner**: Создатель/владелец (внешний ключ на модель «Кастомного пользователя»)

### Model_Message:
- **subject**: Тема письма, ограничение 150 символами
- **body**: Тело письма, без ограничений
- **owner**: Создатель/владелец (внешний ключ на модель «Кастомного пользователя»)

### Model_Mailing:
- **start_time**: Дата и время первой отправки
- **end_time**: Дата и время окончания отправки
- **status**: Статус (строка: 'Завершена', 'Создана', 'Запущена'). Возможные значения:
  - 'done' - рассылка завершена,
  - 'created' - рассылка создана, 
  - 'launched' - рассылка запущена
- **message**: Сообщение (внешний ключ на модель «Сообщение»)
- **recipient**: Получатели («многие ко многим», связь с моделью «Получатель»).
- **owner**: Создатель/владелец (внешний ключ на модель «Кастомного пользователя»)

### Model_SendingAttempt:
- **created_at**: Дата и время попытки
- **status**: Статус (строка: 'Успешно', 'Не успешно'). Возможные значения:
  - 'success' - успешно отправлено,
  - 'fail' - не успешно отправлено,
- **answer**: Ответ почтового сервера (текст)
- **mailing**: Рассылка (внешний ключ на модель «Рассылка»).

[<- на начало](#содержание)

---
## Services client_connect:
### AccessControlService:
Сервисный класс для работы с правами доступа  
Методы:
- can_access_object(user: CustomUser, obj: Model, permission_name: str = None) -> bool:  
Проверяет, имеет ли пользователь право выполнить действие над объектом. Создатель имеет право.
- authorize_access(user: CustomUser, obj: Model, permission_name: str = None) -> Optional[HttpResponseForbidden]:  
Проверяет право доступа пользователя к выполнению действия над объектом.
### MailingService:
Сервисный класс для работы с рассылкой  
Методы:
- update_status(mailing: Mailing, status: str = "created") -> None:  
Обновляет статус рассылки и фиксирует временные метки.
- send_messages(recipients: list, message: Message, mailing: Mailing) -> None:  
Отправляет сообщения получателям и фиксирует результаты.

[<- на начало](#содержание)

---
## Urls client_connect:

- ### recipient(получатель)
  - Список получателей  
  http://127.0.0.1:8000/recipiens/
    - **Доступ:** зарегистрированному пользователю
  - Добавление получателя  
  http://127.0.0.1:8000/recipient/create/
    - **Доступ:** зарегистрированному пользователю
  - Детальная информация о получателе  
  http://127.0.0.1:8000/recipient/(pk)>/detail/
    - где (pk) - это, целое число PrimaryKey, ID получателя
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав
  - Изменение получателя  
  http://127.0.0.1:8000/recipient/(pk)>/edit/
    - где (pk) - это, целое число PrimaryKey, ID получателя
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав
  - Удаление получателя  
  http://127.0.0.1:8000/recipient/(pk)>/delete/
    - где (pk) - это, целое число PrimaryKey, ID получателя
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав

- ### message(сообщение)
  - Список сообщений 
  http://127.0.0.1:8000/messages/
    - **Доступ:** зарегистрированному пользователю
  - Добавление сообщения  
  http://127.0.0.1:8000/message/create/
    - **Доступ:** зарегистрированному пользователю
  - Детальная информация о сообщение   
  http://127.0.0.1:8000/message/(pk)>/detail/
    - где (pk) - это, целое число PrimaryKey, ID сообщения
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав
  - Изменение сообщения  
  http://127.0.0.1:8000/message/(pk)>/edit/
    - где (pk) - это, целое число PrimaryKey, ID сообщения
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав
  - Удаление сообщения  
  http://127.0.0.1:8000/message/(pk)>/delete/
    - где (pk) - это, целое число PrimaryKey, ID сообщения
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав

- ### mailing(рассылка)
  - Список рассылок 
  http://127.0.0.1:8000/mailings/
    - **Доступ:** зарегистрированному пользователю
  - Добавление рассылки  
  http://127.0.0.1:8000/mailing/create/
    - **Доступ:** зарегистрированному пользователю
  - Детальная информация о рассылке  
  http://127.0.0.1:8000/mailing/(pk)>/detail/
    - где (pk) - это, целое число PrimaryKey, ID рассылки
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав
  - Изменение рассылки  
  http://127.0.0.1:8000/mailing/(pk)>/edit/
    - где (pk) - это, целое число PrimaryKey, ID рассылки
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав
  - Удаление рассылки  
  http://127.0.0.1:8000/mailing/(pk)>/delete/
    - где (pk) - это, целое число PrimaryKey, ID рассылки
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав
  - Запуск рассылки 
  http://127.0.0.1:8000/mailing/(pk)>/send/
    - где (pk) - это, целое число PrimaryKey, ID рассылки
    - **Доступ:** зарегистрированному пользователю, создателю и при наличии прав

- ### sending_attempt(рассылка)
  - Запуск рассылки 
  http://127.0.0.1:8000/sending_attempts/
    - **Доступ:** зарегистрированному пользователю

[<- на начало](#содержание)

---
## Views client_connect:

### BaseLoginView:
Базовый класс представления прав доступа к контролерам
- Атрибуты:
  - request (HttpRequest): HTTP-запрос(Объявлен тип для IDE).
  - kwargs (dict): Ключевые аргументы запроса(Объявлен тип для IDE).
  - model (Type[models.Model]): Модель для обработки запросов.
  - queryset (QuerySet): Набор данных для обработки запросов.  
- Методы:
  - get_queryset(self) -> QuerySet:  
  Получение набора данных для обработки запроса.  
  raise NotADirectoryError: Если в подклассе не указана модели или queryset
  - get_object(self) -> models.Model:  
  Получение объекта по первичному ключу из URL.  
  raise Http404("pk не передан в URL")
  - dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponseBase:  
  Проверка прав доступа перед обработкой запроса
  - get_permission_name(self) -> str:  
  Метод заполняемы в подклассе, для передачи названия доступа.  
  raise NotADirectoryError: Если в подклассе не реализован метод

### RecipientsListViews:
Класс отвечающий за представление списка получателей.
Отображает список получателей в шаблоне recipients_list.html.
Порядок отображения получателей - email  
- Методы:
  - get_queryset(self) -> QuerySet:  
  Переопределение метода get_queryset для получения списка получателей.
  Пользователь видит только своих получателей.
### MessagesListView:
Класс отвечающий за представление списка сообщений.
Отображает список сообщений в шаблоне messages_list.html.
Порядок отображения сообщений - subject  
- Методы:
  - get_queryset(self) -> QuerySet:
  Переопределение метода get_queryset для получения списка сообщений.
  Пользователь видит только свои сообщения.
### MailingsListView:
Класс отвечающий за представление списка рассылок.
Отображает список рассылок в шаблоне mailings_list.html.
Порядок отображения рассылок - created_at по убыванию  
- Методы:
  - get_queryset(self) -> QuerySet:  
  Переопределение метода get_queryset для получения списка рассылок.
  Пользователь видит только свои рассылки.
### SendingAttemptsListView:
Класс отвечающий за представление списка попыток рассылок.
Отображает список рассылок в шаблоне sending_attempts_list.html.
Порядок отображения рассылок - mailing и created_at по убыванию  
Методы:
- get_queryset(self) -> QuerySet:  
Переопределение метода get_queryset для получения списка попыток рассылок. 
Пользователь видит только свои рассылки.

### RecipientCreateView:
Представление отвечающее за создание получателя
Методы:
- form_valid(self, form: RecipientForm) -> HttpResponse:  
Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
### RecipientDetailView: 
Представление отвечающее за детальную информацию о получателе.
Методы:
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_recipient"
### RecipientUpdateView:
Представление отвечающее за редактирование получателя.
Методы:
- get_success_url(self) -> HttpResponse:  
Перехож на страницу измененного получателя
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_recipient"
### RecipientDeleteView:
Представление отвечающее за удаление получателя
Методы:
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_recipient"

### MessageCreateView:
Представление отвечающее за создание сообщения
Методы:
- form_valid(self, form: MessageForm) -> HttpResponse:  
Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
### MessageDetailView:
Представление отвечающее за детальную информацию о сообщения
Методы:
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.view_message"
### MessageUpdateView:
Представление отвечающее за редактирование сообщения
Методы:
- get_success_url(self) -> HttpResponse:  
Перехож на страницу измененного сообщения
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_message"
### MessageDeleteView:
Представление отвечающее за удаление сообщения
Методы:
- get_permission_name(self) -> str:
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"

### MailingCreateView:
Представление отвечающее за создание рассылки
Методы:
- form_valid(self, form: MailingForm) -> HttpResponse:  
Обрабатывает форму, ели она действительна, устанавливает владельца текущего пользователя
- get_form(self, form_class: Optional[BaseForm] = None) -> BaseForm:  
Возвращает форму с фильтрованными полями message и recipients, по текущему пользователю
### MailingDetailView:
Представление отвечающее за детальную информацию о рассылки
Методы:
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"
### MailingUpdateView:
Представление отвечающее за редактирование рассылки
Методы:
- get_success_url(self) -> HttpResponse:  
Перехож на страницу измененной рассылки
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_message"
- get_form(self, form_class: Optional[BaseForm] = None) -> BaseForm:  
Возвращает форму с фильтрованными полями message и recipients, по текущему пользователю
### MailingDeleteView:
Представление отвечающее за удаление рассылки
Методы:
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.delete_message"

### HomeViews:
Представление для отображения информации о рассылках  
Методы:
- get_context_data(self, **kwargs) -> dict:  
Заносит в контекст все рассылки, рассылки со статусом 'запущено' и уникальных получателей. 
Для пользователя не входящего в группы и не являющего супер пользователем выводит только свои данные.

### MailingSendView:
Представление отвечающее за отправку рассылки
Методы:
- post(self, request: HttpRequest, pk: int) -> HttpResponse:  
Обработка пост запроса запуска рассылки.
- get_permission_name(self) -> str:  
Метод для передачи названия доступа в родительский класс BaseLoginView: "client_connect.change_mailing"

[<- на начало](#содержание)

---
# Приложение users:
## Admin users
### CustomUserAdmin
Класс для работы администратора с кастомными пользователями
Атрибуты:
- ordering - сортировка по логику
- list_filter - фильтрация активный пользователь или нет
- exclude - исключит поле пароля
- list_display - выводит на экран: логин, email, имя, фамилия, активный
- search_fields - поиск по: логин, email

[<- на начало](#содержание)

---
## Forms users
### CustomUserCreationForm:
Кастомная форма регистрации пользователя.  
Атрибуты:
- username(str): Логин пользователя, обязательный параметр
- usable_password: Устанавливает параметр для управления паролем
Методы:
- __init__(self, *args, **kwargs) -> None:  
Инициализирует поля формы с пользовательскими настройками и атрибутами.
### UserUpdateForm:
Форма изменения данных пользователя.  
Методы:
- __init__(self, *args, **kwargs) -> None:  
Инициализирует поля формы с пользовательскими настройками и атрибутами.
### CustomAuthenticationForm:
Кастомная форма авторизации пользователя
Методы:
- __init__(self, *args, **kwargs) -> None:
Инициализирует поля формы с пользовательскими настройками и атрибутами
- clean_username(self) -> str:  
Проверка наличие пользователя логином.  
:raise ValidationError: Если пользователь не зарегистрирован.
### PasswordRecoveryForm:
Форма регистрации пользователя.
Атрибуты:
- email(str): форма email без ограничений  
Методы:
- __init__(self, *args, **kwargs) -> None:  
Инициализирует поля формы с пользовательскими настройками и атрибутами.
- clean_email(self) -> str:  
Проверка на существования email.  
:raise ValidationError: Если пользователя не существует в БД
### NewPasswordForm:
Форма обновления пароля.  
Методы:
- __init__(self, *args, **kwargs) -> None:  
Инициализирует поля формы с пользовательскими настройками

[<- на начало](#содержание)

---
## Models users
### CustomUser:
Представление кастомного пользователя, расширяющее AbstractUser.
Email обязательное поле при авторизации.
Атрибуты:
- email(str): Уникальный email
- avatar(ImageField): Аватар (изображение)
- phone_number(str): Номер телефона
- country(str): Страна
- token(str): Токен для активации

[<- на начало](#содержание)

---
## Services users
### CustomUserService
Сервисное класс для работы с пользователями
Методы:
- activate_by_email(token: str) -> CustomUser:  
Активация пользователя по токену через email.
- send_email(subject: str, message: str, user_emails: list) -> None:  
Отправка письма на email

[<- на начало](#содержание)

---
## Urls users:
- **Страница списка пользователей**
http://127.0.0.1:8000/users/
- **Страница авторизации:**  
http://127.0.0.1:8000/users/login/
- **Страница детальной информации о пользователе**
http://127.0.0.1:8000/users/(pk)/detail/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- **Страница изменения данных пользователя**
http://127.0.0.1:8000/users/edit/
- **Страница регистрации:**  
http://127.0.0.1:8000/users/register/
- **Страница выхода из аккаунта**  
http://127.0.0.1:8000/users/logout/
- **Страница подтверждения email**  
http://127.0.0.1:8000/users/email_confirm/(token)/
  - где (token) - это, строка токена
- **Страница восстановления пароля**
http://127.0.0.1:8000/users/password-reset/
- **Страница успешной отправки и инструкция для восстановления пароля**
http://127.0.0.1:8000/users/password-reset/done/
- **Страница обновления пароля пользователя**
http://127.0.0.1:8000/users/password-reset/(uidb64)/(token)/  
  где, 
  - (token) - это строка токена
  - (uidb64) - это закодированный PK пользователя
- **Страница успешного изменения пароля**
http://127.0.0.1:8000/users/password-reset/complete/
- **Страница активации пользователя**
http://127.0.0.1:8000/users/(pk)/activation/
  - где (pk) - это, целое число PrimaryKey, ID пользователя
- **Страница деактивации пользователя**
http://127.0.0.1:8000/users/(pk)/deactivate/
  - где (pk) - это, целое число PrimaryKey, ID пользователя

[<- на начало](#содержание)

---
## Views users:
### RegisterView:
Кастомное представление регистрации пользователя
При успешной валидации отправляет письмо пользователю для подтверждения email
Методы:
- form_valid(self, form: ModelForm) -> HttpResponse:  
Обрабатывает валидную форму и выполняет дополнительное действие
- send_confirmation_email(self, user_email: str, token: str) -> None:  
Отправляет письма с токеном для подтверждения почты
### UserActivationView:
Представление активации пользователя
Методы:
- get(self, request: HttpRequest, token: str) -> HttpResponse:  
Обрабатывает GET запрос для активации пользователя по токену.
- email_verification(self, token: str) -> HttpResponse:  
Активация пользователя по токену.
### PasswordRecoveryView:
Представление для восстановления пароля по email.  
Методы:
- post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:  
Обрабатывает отправку формы с email
- send_password_recovery_email(self, user: CustomUser, token: str) -> None:  
Отправляет электронное письмо для восстановления пароля.
### NewPassword:
Представление для сброса пароля пользователя, содержащий uidb64 и токен.
Методы:
- dispatch(request: HttpRequest, *args, **kwargs) -> HttpResponse:  
Обрабатывает входящие параметры URL и проверяет их валидность.
- get_form_kwargs() -> dict:  
Передает объект пользователя в форму для установки нового пароля.
### UserDetailView:
Представление отвечающее за детальную информацию о пользователе
### UserUpdateView:
Представление обновления данных пользователя.
### CustomLoginView:
Кастомное представление регистрации пользователя
### UsersListView:
Представление отвечающее за получения списка пользователей.  
Методы:
- get_queryset(self) -> QuerySet:  
Переопределение метода get_queryset, для получения списка пользователей отсортированных по логину:
без супер юзеров, сотрудников и пользователей входящих в группы.
### ActivationUserView:
Представление отвечающее за активацию пользователя.
Активировать возможно с правом can_deactivate_user.  
Методы:
- post(self, request: HttpRequest, pk: int) -> HttpResponse:  
Пост запрос на активацию пользователя
### DeactivateUserView:
Представление отвечающее за деактивацию пользователя.
Деактивировать возможно с правом can_deactivate_user.  
Методы:
- post(self, request: HttpRequest, pk: int) -> HttpResponse:  
Пост запрос на деактивацию пользователя

[<- на начало](#содержание)
