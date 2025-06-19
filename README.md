# Проект "Веб-приложение с помощью Django"

## Содержание:
- [Описание](#описание)
- [Проверить версию Python](#проверить-версию-python)
- [Установка Poetry](#установка-poetry)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Структура проекта](#структура-проекта)
- [Приложение client_connect](#приложение-client_connect)
  - [Admin client_connect](#admin-client_connect)
    - ...
  - [Models client_connect](#models-client_connect)
    - [Model_Recipient](#model_recipient)
    - [Model_Message](#model_message)
    - [Model_Mailing](#model_mailing)
    - [Model_SendingAttempt](#model_sendingattempt)
  - [Urls client_connect](#urls-client_connect)
  - [Views client_connect](#views-client_connect)
    - ...

   
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
poetry add python-dotenv psycopg2
poetry add --group lint flake8 black isort mypy ipython
poetry add --group dev django
```
- Зайдите в файл .env.example и следуйте инструкция

[<- на начало](#содержание)


## Запуск проекта:
Чтобы запустить сервер разработки, выполните следующую команду:
```bash
python manage.py runserver
```

[<- на начало](#содержание)


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
|   |   |   ├── base.html # базовый шаблон
|   |   |   ├── ___ # ___
|   |   |   └── header.html # верхняя часть страницы(меню)
|   ├── __init__.py
|   ├── admin.py # регистрация моделе в админке
|   ├── apps.py
|   ├── models.py # модели БД
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
|   |   └── ___
|   └── js/
|   |   └── ___
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
### ...Admin
...
[<- на начало](#содержание)


## Models client_connect:
- **Recipient**: Представление получателя
- **Message**: Представление сообщения
- **Mailing**: Представление рассылки
- **SendingAttempt**: Представление попытки рассылки

[<- на начало](#содержание)

### Model_Recipient:
- **email**: Электронная почта, уникальная
- **full_name**: Ф.И.О., ограничение 150 символами
- **comment**: Комментарий, без ограничений

[<- на начало](#содержание)

### Model_Message:
- **subject**: Тема письма, ограничение 150 символами
- **body**: Тело письма, без ограничений

[<- на начало](#содержание)

### Model_Mailing:
- **created_at**: Дата и время первой отправки
- **update_at**: Дата и время окончания отправки
- **status**: Статус (строка: 'Завершена', 'Создана', 'Запущена'). Возможные значения:
  - 'done' - рассылка завершена,
  - 'created' - рассылка создана, 
  - 'launched' - рассылка запущена
- **message**: Сообщение (внешний ключ на модель «Сообщение»)
- **recipient**: Получатели («многие ко многим», связь с моделью «Получатель»).

[<- на начало](#содержание)

### Model_SendingAttempt:
- **created_at**: Дата и время попытки
- **status**: Статус (строка: 'Успешно', 'Не успешно'). Возможные значения:
  - 'suc' - успешно отправлено,
  - 'fail' - не успешно отправлено,
- **answer**: Ответ почтового сервера (текст)
- **mailing**: Рассылка (внешний ключ на модель «Рассылка»).

[<- на начало](#содержание)


## Urls client_connect:
- ...

[<- на начало](#содержание)


## Views client_connect:
### ...:
...

[<- на начало](#содержание)


---
