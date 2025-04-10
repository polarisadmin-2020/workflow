"""RabbitMQ Consumer for BSON messages."""

import json
import os
import sys
import time

import django
import mongoengine
import pika
from bson import ObjectId
from django.conf import settings
from django.apps import apps
from mongoengine.errors import ValidationError

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields to strings in a dictionary."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(v) for v in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data


def get_mongoengine_models():
    """Retrieve all MongoEngine document classes from all installed apps."""
    models = {}
    try:
        for app_config in apps.get_app_configs():
            try:
                module = __import__(f"{app_config.name}.models", fromlist=["*"])
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, mongoengine.Document)
                        and attr is not mongoengine.Document
                    ):
                        models[attr.__name__] = attr
            except (ModuleNotFoundError, ImportError):
                continue
    except Exception as e:
        print(f"Error retrieving MongoEngine models: {str(e)}")
    return models


def process_message(model_name, data, action):
    """Process messages from RabbitMQ (insert/update/delete) dynamically."""
    try:
        models = get_mongoengine_models()

        if model_name not in models:
            print(f"Error: Unknown model '{model_name}' received.")
            return

        ModelClass = models[model_name]

        # Convert ObjectId fields to strings (deeply)
        data = convert_objectid_to_str(data)

        # Get the primary key field for this model (usually 'id' unless overridden)
        pk_field = ModelClass._meta["id_field"]

        # Try to extract the primary key value from the incoming data
        obj_id = data.get(pk_field) or data.get("_id") or data.get("id")
        if not obj_id:
            print(f"Warning: No ID found for model '{model_name}'. Skipping.")
            return

        # Remove ID fields to avoid duplication
        data.pop("_id", None)
        data.pop("id", None)

        # Delete operation
        if action == "delete":
            result = ModelClass.objects(**{pk_field: obj_id}).delete()
            print(f"Deleted {result} {model_name}(s) with {pk_field}={obj_id}")
            return

        # Filter out unknown fields
        valid_fields = ModelClass._fields.keys()
        clean_data = {k: v for k, v in data.items() if k in valid_fields}

        # Update if exists
        obj = ModelClass.objects(**{pk_field: obj_id}).first()
        if obj:
            obj.modify(**clean_data)
            print(f"Updated {model_name} with {pk_field}={obj_id}")
        else:
            clean_data[pk_field] = obj_id
            obj = ModelClass(**clean_data)
            obj.save()
            print(f"Created new {model_name} with {pk_field}={obj_id}")

    except ValidationError as ve:
        print(f"Validation error in {model_name}: {str(ve)}")
    except Exception as e:
        print(f"Error processing {model_name}: {str(e)}")


def start_consumer():
    """Start RabbitMQ Consumers for all queues in settings."""
    queues = getattr(settings, "RABBITMQ_QUEUES_BSON", [])

    if isinstance(queues, str):
        queues = [q.strip() for q in queues.split(",") if q.strip()]

    if not queues:
        print("No RabbitMQ BSON queues defined. Exiting.")
        return

    credentials = pika.PlainCredentials(
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASSWORD,
    )

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    credentials=credentials,
                )
            )
            channel = connection.channel()

            for queue_name in queues:
                channel.queue_declare(queue=queue_name, durable=True)

                def make_callback(queue):
                    def callback(ch, method, properties, body):
                        try:
                            message = json.loads(body)
                            model_name = message.get("model")
                            data = message.get("data")
                            action = message.get("action", "save")
                            process_message(model_name, data, action)
                            ch.basic_ack(delivery_tag=method.delivery_tag)
                        except json.JSONDecodeError:
                            print(f"[{queue}] Error: Unable to decode JSON.")
                            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                        except Exception as e:
                            print(f"[{queue}] Error: {str(e)}")
                            ch.basic_nack(delivery_tag=method.delivery_tag)
                    return callback

                channel.basic_consume(
                    queue=queue_name,
                    on_message_callback=make_callback(queue_name),
                )

            print(f"Listening for BSON messages on: {', '.join(queues)}")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ connection lost. Reconnecting in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    try:
        print("Starting RabbitMQ consumer...")
        start_consumer()
    except KeyboardInterrupt:
        print("Consumer stopped manually.")
    except Exception as e:
        print(f"Critical error: {str(e)}")
