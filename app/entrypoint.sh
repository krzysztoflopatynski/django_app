#!/bin/sh

if [ "$DATABASE" = "mariadb" ]
then
    echo "Waiting for mariadb..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "MariaDB started"
fi

python manage.py migrate
python manage.py collectstatic --no-input
daphne -b 0.0.0.0 -p 8000 django_app.asgi:application
exec "$@"