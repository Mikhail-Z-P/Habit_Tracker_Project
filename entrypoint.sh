#!/bin/sh

echo "Применение миграций..."
python manage.py migrate --noinput

echo "Сбор статики..."
python manage.py collectstatic --noinput

echo "Запуск Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
