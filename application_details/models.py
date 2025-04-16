"""Models for the application_details app."""

from mongoengine import StringField, DynamicDocument


class Application(DynamicDocument):
    """Stores application information for different field types."""

    application_number = StringField(required=True, unique=True)
    status = StringField(required=True)
    created_at = StringField()
    meta = {
        "collection": "application",
        "indexes": [
            {
                "fields": ["application_number"],
                "unique": True,
            },
        ],

        "ordering": ["-created_at"]  # Default ordering by created_date (descending)

    }