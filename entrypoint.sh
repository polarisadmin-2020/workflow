#!/usr/bin/env sh

python manage.py migrate
#python manage.py runserver 0.0.0.0:8004
python manage.py collectstatic --no-input
python -m gunicorn core.wsgi:application --bind 0.0.0.0:8004 --workers 4 --access-logfile - --error-logfile - --log-level debug
 
 