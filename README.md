# FOODGRAM - Продуктовый помощник

Стек технологий

Python, Django, Django, REST Framework, PostgreSQL, Nginx, gunicorn, 
docker, GitHub, Yandex.Cloud.

Описание проекта

Foodgram это ресурс для публикации рецептов.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей,
подписываться на интересных авторов, добавлять лучшие рецепты в избранное, 
а также создавать список покупок и загружать его в pdf формате

Установка проекта локально
Склонировать репозиторий на локальную машину:
git clone https://github.com/px2005/foodgram-project-react.git

cd foodgram-project-react
Cоздать и активировать виртуальное окружение:
python -m venv env
source env/bin/activate
Cоздайте файл .env в директории /infra/ с содержанием:
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
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
контейнер приложения backend
контейнер web-сервера nginx
Примените миграции:
docker-compose exec backend python manage.py migrate
Создайте администратора:
docker-compose exec backend python manage.py createsuperuser
Соберите статику:
docker-compose exec backend python manage.py collectstatic --noinput
