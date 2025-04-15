#!/usr/bin/env sh

python manage.py migrate
#python manage.py runserver 0.0.0.0:8000
python manage.py collectstatic --no-input

echo "Starting Django..."
python -m gunicorn core.wsgi:application --bind 0.0.0.0:8004 --workers 4 --access-logfile - --error-logfile - --log-level debug &

sleep 3

echo "Starting RabbitMQ Consumers..."

# Start both consumers in background
python rabbitmq/consumer_BSON.py || { echo "Failed to start consumer_BSON"; exit 1; } &
python rabbitmq/consumer.py || { echo "Failed to start consumer"; exit 1; } &

# Wait for all background processes
wait
