# Foodgram - «Продуктовый помощник»

Foodgram это сайт, где люди могут публиковать свои рецепты, узнать рецепты 
других пользователей, подписываться на интересных авторов, 
добавлять лучшие рецепты в избранное,
а также создавать список покупок и загружать его в pdf формате


## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)


# Запуск и работа с проектом
Чтобы развернуть проект, вам потребуется:
1) Клонировать репозиторий git clone https://github.com/px2005/foodgram-project-react.git
2) Создать файл ```.env``` в папке проекта _/infra/_ и заполнить его всеми ключами:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=<ваш_django_secret_key>
```
3) Собрать контейнеры:
```python
cd foodgram-project-react/infra
docker-compose up -d --build
```
4) Сделать миграции, собрать статику и создать суперпользователя:
```python
docker-compose exec -T web python manage.py makemigrations users --noinput
docker-compose exec -T web python manage.py makemigrations recipes --noinput
docker-compose exec -T web python manage.py migrate --noinput
docker-compose exec -T web python manage.py collectstatic --no-input
docker-compose exec web python manage.py createsuperuser
```


### Авторы
Александр Горыничев

px2005@yandex.ru
