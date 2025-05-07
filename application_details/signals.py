"""Signal handlers for application_details app."""

from bson import ObjectId
from mongoengine import signals

from application_details.models import Application
from rabbitmq.publisher import RabbitMQPublisher


def convert_objectid_to_str(data):
    """Recursively convert ObjectId fields to strings in a dictionary or list."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(v) for v in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data


def publish_application(sender, document, **kwargs):
    """Publish Application changes to RabbitMQ."""
    try:
        publisher = RabbitMQPublisher()
        data = convert_objectid_to_str(document.to_mongo().to_dict())

        publisher.send(
            model_name="Application",
            data=data,
            queue_name="application-updates",  # Consistent with your other code
            action="update",
        )
        publisher.close()
        print(f"Published update for Application: {data.get('application_number')}")

    except Exception as e:
        print(f"Error publishing Application update: {str(e)}")


signals.post_save.connect(publish_application, sender=Application)
