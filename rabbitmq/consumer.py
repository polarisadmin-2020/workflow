"""RabbitMQ Consumer to save messages to the database."""

import json
import os
import sys
import time

import django
import pika
from django.apps import apps
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist

# Django setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def process_message(body: any) -> None:
    """Process received messages based on the app and model."""
    data = json.loads(body)

    full_model_name = data.get("model")  # Expected format: "app_label.ModelName"
    if not full_model_name or "." not in full_model_name:
        print("Error: Model name must be in 'app_label.ModelName' format.")
        return

    try:
        app_label, model_name = full_model_name.split(".")
        ModelClass = apps.get_model(app_label, model_name)
    except (ValueError, LookupError) as e:
        print(f"Error: Could not load model '{full_model_name}': {str(e)}")
        return

    data.pop("model", None)
    clean_data = {}

    for field_name, field_value in data.items():
        try:
            field = ModelClass._meta.get_field(field_name)

            if isinstance(field, django.db.models.ImageField) and field_value:
                clean_data[field_name] = f"{app_label}/{field_value}"

            elif field.is_relation and field_value is not None:
                RelatedModel = field.related_model
                related_pk_field = RelatedModel._meta.pk.name
                related_instance = RelatedModel.objects.filter(
                    **{related_pk_field: field_value}
                ).first()

                if not related_instance:
                    print(
                        f"Warning: {RelatedModel.__name__} with {related_pk_field}={field_value} does not exist."
                    )
                    continue

                clean_data[field_name] = related_instance

            else:
                clean_data[field_name] = field_value

        except FieldDoesNotExist:
            print(f"Skipping unknown field: {field_name}")
        except Exception as e:
            print(f"Error processing field '{field_name}': {e}")

    unique_identifier = data.get("id")
    if not unique_identifier:
        print("Error: Missing unique identifier in the message.")
        return

    try:
        obj, created = ModelClass.objects.update_or_create(
            id=unique_identifier,
            defaults=clean_data,
        )
        print(f"{'Created' if created else 'Updated'} {full_model_name}: {obj}")
    except Exception as e:
        print(f"Error saving the model: {str(e)}")


def consume_queue(queue_name: str) -> None:
    """Consume messages from a specific queue."""
    while True:
        try:
            credentials = pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD,
            )
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=credentials,
                ),
            )
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)

            def callback(ch, method, properties, body):
                try:
                    process_message(body)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    print(f"Error in queue '{queue_name}': {e}")
                    ch.basic_ack(delivery_tag=method.delivery_tag)

            print(f"[✓] Listening on queue: {queue_name}")
            channel.basic_consume(queue=queue_name, on_message_callback=callback)
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print(
                f"[x] Connection lost for queue '{queue_name}'. Reconnecting in 5s..."
            )
            time.sleep(5)


def start_consumer():
    """Start RabbitMQ consumer for each queue in RABBITMQ_QUEUES."""
    queue_list = getattr(settings, "RABBITMQ_QUEUES", [])

    if isinstance(queue_list, str):
        queue_list = [q.strip() for q in queue_list.split(",") if q.strip()]

    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASSWORD,
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=credentials,
        )
    )
    channel = connection.channel()

    for queue_name in queue_list:
        channel.queue_declare(queue=queue_name, durable=True)

        def make_callback(queue):
            def callback(ch, method, properties, body):
                try:
                    process_message(body)  # ✅ fixed: pass full message
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except json.JSONDecodeError:
                    print(f"[{queue}] Error decoding JSON.")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                except Exception as e:
                    print(f"[{queue}] Error: {str(e)}")
                    ch.basic_nack(delivery_tag=method.delivery_tag)

            return callback

        channel.basic_consume(
            queue=queue_name,
            on_message_callback=make_callback(queue_name),
        )

    print(f"Started consumers for: {', '.join(queue_list)}")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        print("Starting RabbitMQ consumer...")
        start_consumer()
    except KeyboardInterrupt:
        print("Consumer stopped manually.")
    except Exception as e:
        print(f"Critical error: {str(e)}")
