# FOODGRAM - Продуктовый помощник

server: http://62.84.122.171
http://px2005.ddns.net

Пользователи:
E-mail: admin2@foodgram.com
Password: Asdfgh456
E-mail:: user@foodgram.com
Password: Zxcvbn456

Стек технологий

Python, Django, Django, REST Framework, PostgreSQL, Nginx, gunicorn,
docker, GitHub, Yandex.Cloud.

Описание проекта

Foodgram это сайт, где люди могут публиковать свои рецепты, узнать рецепты 
других пользователей, подписываться на интересных авторов, 
добавлять лучшие рецепты в избранное,
а также создавать список покупок и загружать его в pdf формате

Установка проекта локально
Склонировать репозиторий на локальную машину:

git clone https://github.com/px2005/foodgram-project-react.git

cd foodgram-project-react

Cоздать и активировать виртуальное окружение:

python -m venv env

source env/bin/activate

Cоздайте файл .env в директории /infra/ с содержанием:

DB_ENGINE=django.db.backends.postgresql

DB_NAME=postgres

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

DB_HOST=db

DB_PORT=5432

SECRET_KEY='xxxxxxxx'

ALLOWED_HOSTS=['*', 'web', '62.84.122.171', '127.0.0.1']


Перейти в директирию и установить зависимости из файла requirements.txt:

cd backend/

pip install -r requirements.txt

Выполните миграции:

python manage.py migrate

Запустите сервер:

python manage.py runserver

Запуск проекта в Docker контейнере

Установите Docker.

Параметры запуска описаны в файлах docker-compose.yml и nginx.conf,

которые находятся в директории infra/.

При необходимости добавьте/измените адреса проекта в файле nginx.conf

Запустите docker compose:

docker-compose up -d --build

После сборки появляются 3 контейнера:

контейнер базы данных db

контейнер приложения web

контейнер web-сервера nginx

Примените миграции:

docker-compose exec web python manage.py migrate

Создайте администратора:

docker-compose exec web python manage.py createsuperuser

Соберите статику:

docker-compose exec web python manage.py collectstatic --noinput
