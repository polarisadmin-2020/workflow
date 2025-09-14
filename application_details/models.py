"""Models for the application_details app."""

from mongoengine import DynamicDocument, StringField


class Application(DynamicDocument):
    """Stores application information for different field types."""

    application_number = StringField(required=True, unique=True)
    status = StringField(required=True)
    position_id = StringField(required=False, help_text="ID of the position handling this application")
    created_at = StringField()
    meta = {
        "collection": "application",
        "indexes": [
            {
                "fields": ["application_number"],
                "unique": True,
            },
        ],
        "ordering": ["-created_at"],  # Default ordering by created_date (descending)
    }
