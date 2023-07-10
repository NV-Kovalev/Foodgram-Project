### Проект Foodgram

![example workflow](https://github.com/atar1boy/foodgram-project-react/actions/workflows/deploy_workflow.yml/badge.svg)

## Сервис позволяющий пользователям создавать рецепты, подписываться на любимых авторов и подготавливать список покупок из понравившихся рецептов.

## Команда разработчиков:
backend: Никита Ковалев
frontend: Yandex Practicum

## Используемые технолологии:

Django
Django REST Framework
PostgreSQL
Nginx
gunicorn
Docker

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:atar1boy/foodgram-project-react
```

Создать .env файл внутри директории infra (на одном уровне с docker-compose.yaml) Пример .env файла:

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

* По желанию можно загрузить в базу данных тестовые данные или только ингредиенты:

Ингредиенты:

    ```
    docker-compose exec django python3 manage.py shell
    from data import load_data
    load_data.fill_ingredients_from_csv()
    quit()
    ```

Тестовые данные:

    ```
    docker-compose exec django python3 manage.py loaddata db.json
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
http://localhost/admin/
```

```
Логин: adminfoodgram@yandex.ru
Пароль: admin2023
```