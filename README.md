# Проект "Веб-приложение с помощью Django"

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
    - ...
  - [Urls client_connect](#urls-client_connect)
  - [Views client_connect](#views-client_connect)
    - ...

   
## Описание:

Разработка приложения(веб-сайта) с рассылкой сообщений, с помощью фреймворка Django.

## Проверить версию Python:

Убедитесь, что у вас установлен Python (версия 3.x). Вы можете проверить установленную версию Python, выполнив команду:
```
python --version
```

## Установка Poetry:
Если у вас еще не установлен Poetry, вы можете установить его, выполнив следующую команду
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Проверить Poetry добавлен в ваш PATH.
```bash
poetry --version
```

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

## Запуск проекта:
Чтобы запустить сервер разработки, выполните следующую команду:
```bash
python manage.py runserver
```

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

---
# Приложение client_connect:
## Admin client_connect
### ...Admin
...


## Models client_connect:
- ...
### Model_...
...


## Urls client_connect:
- ...


## Views client_connect:
### ...:
...


---
