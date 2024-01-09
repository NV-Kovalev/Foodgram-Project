# Foodgram

![example workflow](https://github.com/atar1boy/foodgram-project-react/actions/workflows/deploy_workflow.yml/badge.svg)

## Мой дипломный проект демонстрирующий мои знания в работе с Django, Docker, CI/DI. Сейчас доступа к проекту нет, но если будет желание его увидеть, то пишите мне в личку. Контакты можно найти здесь в readme и в моем профиле.

### Контакты: [t.me/gl_ready/](https://t.me/gl_ready/)

## Используемые технолологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-005571?style=for-the-badge&logo=Django)
![Docker](https://img.shields.io/badge/Docker-%2300f.svg?style=for-the-badge&logo=Docker)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-3ECF8E?style=for-the-badge&logo=PostgreSQL)

## Как запустить проект:

Создать .env файл внутри директории infra (на одном уровне с docker-compose.yml) Пример .env файла:

```
SECRET_KEY = 'secret_key'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=host1,host2
CSRF_TRUSTED_ORIGINS=http://host1,https://host2
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Запуск Docker контейнеров: Запустите docker-compose:

```
cd infra/
docker-compose up -d --build
```

Выполните миграции:
```
docker-compose exec django python manage.py makemigrations
docker-compose exec django python manage.py migrate
```

Cоздайте суперпользователя:

```
docker-compose exec django python manage.py createsuperuser
```

Подготовьте статику:

```
docker-compose exec django python manage.py collectstatic --no-input 
```

## База данных:

* По желанию можно загрузить мой бэкап в базу данных:

Ингредиенты:

    ```
    docker-compose exec django python3 manage.py shell
    from data import load_data
    load_data.fill_ingredients_from_csv()
    quit()
    ```

Тестовые данные:

    ```
    docker-compose exec django python3 manage.py loaddata newdb.json
    ```

## Проект будет полностью доступен по ссылке:

```
http://localhost/
```

## Документация:

```
http://localhost/api/docs/
```

## Админка:

```
URL: http://158.160.57.117/admin/
Логин: adminfoodgram@yandex.ru
Пароль: admin2023
```

