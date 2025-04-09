"""Models for the application_details app."""

from typing import Type

from django.utils.timezone import now
from mongoengine import StringField, Document


class Application(Document):
    """Stores application information for different field types."""

    application_number = StringField(required=True, unique=True)
    status = StringField(required=True)
    meta = {
        "collection": "application",
        "indexes": [
            {
                "fields": ["application_number"],
                "unique": True,
            },
        ],
    }  # Define MongoDB collection name
