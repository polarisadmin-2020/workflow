"""Publish MongoDB documents to RabbitMQ."""

import json

import pika
from django.conf import settings


class RabbitMQPublisher:
    """Class to publish messages to RabbitMQ."""

    def __init__(self: "RabbitMQPublisher") -> None:
        """Initialize the RabbitMQ connection."""
        try:
            credentials = pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD,
            )
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=credentials,
                ),
            )
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None

    def send(self, model_name, data, action="save", queue_name="Application_queue"):
        """Send a message to RabbitMQ with an action."""
        message = json.dumps(
            {
                "model": model_name,
                "data": data,
                "action": action,
            },
        )

        self.channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )

        print(f"Sent {action.upper()} event for {model_name} to RabbitMQ.")

    def close(self: "RabbitMQPublisher") -> None:
        """Close the RabbitMQ connection."""
        if self.connection:
            self.connection.close()
