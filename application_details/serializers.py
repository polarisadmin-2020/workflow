"""Configuration serializers."""

from rest_framework import serializers


class DynamicApplicationSerializer(serializers.Serializer):
    """Serializer for Application to validate and store JSON data."""

    def to_representation(self, obj):
        """Convert the MongoEngine document to a dict"""
        data = obj.to_mongo().to_dict()
        data["id"] = str(data.pop("_id"))  # Optional: Convert ObjectId to string
        return data

    def update(self, instance, validated_data):
        """Update the MongoEngine document with the validated data."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
