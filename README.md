### Для чего этот проект?!
Проект YaMDb собирает отзывы пользователей на произведения.
В данном проекте описан API для работы с YaMDb.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:apaffka/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Документация к API проекта Yatube (v1)

К проекту подключен REDOC: http://127.0.0.1:8000/redoc/
Там вы можете ознакомиться с эндпоинтами и методами, а также с примерами запросов, ответов и кода.
