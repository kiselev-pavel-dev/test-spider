# Тестовое задание для компании Spider

# Технологии:
    Python 3.10
    Django 4.1.2
    Django Rest Framework 3.14.0
    PostgreSQL
    Docker
    Redoc
    Pytest


# Запуск и работа с проектом
Чтобы развернуть проект, вам потребуется:
1) Клонировать репозиторий GitHub:
```python
git clone https://github.com/kiselev-pavel-dev/test-spider.git
```
2) Перейти в папку с проектом
```python
cd test-spider
```

3) Создать и активировать виртуальное окружение, установить зависимости
```python
python -m venv venv
source venv/scripts/activate (Windows)
pip install -r requirements.txt
```
4) Создать файл ```.env``` в корневой папке проекта и заполнить его всеми ключами:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

5) Собрать контейнеры:
```python

docker-compose up -d --build
```

6) Сделать миграции, собрать статику и создать суперпользователя:
```python
docker-compose exec -T web python manage.py makemigrations --noinput
docker-compose exec -T web python manage.py migrate --noinput
docker-compose exec -T web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```

Теперь можно зайти в админку _http://localhost/admin/_ под вашим логином администратора.


# Документация API.
По адресу http://localhost/redoc/ Вы можете увидеть полную документацию по API

# Тестирование
Чтобы выполнить тестирование необходимо перейти в папку spider и выполнить:
```python
pytest
```

### <br /> Автор проекта:
Киселев Павел<br />
neznika2@mail.ru<br />
