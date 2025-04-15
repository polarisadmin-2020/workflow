#!/usr/bin/env sh

python manage.py migrate
#python manage.py runserver 0.0.0.0:8000
python manage.py collectstatic --no-input

echo "Starting Django..."
python -m gunicorn core.wsgi:application --bind 0.0.0.0:8004 --workers 4 --access-logfile - --error-logfile - --log-level debug &

sleep 3

# Start the RabbitMQ Consumers
echo "Starting RabbitMQ Consumers..."
exec python rabbitmq/consumer_BSON.py || { echo "Failed to start RabbitMQ Consumer"; exit 1; }
python rabbitmq/consumer.py &
wait
