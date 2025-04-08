"""Configuration serializers."""

from typing import Any, Dict

from rest_framework import serializers

from .models import Application


class ApplicationSerializer(serializers.Serializer):
    """Serializer for application_details."""

    application_number = serializers.CharField()
    status = serializers.CharField()

    def update(
        self,
        instance: Application,
        validated_data: Dict[str, Any],
    ) -> Application:
        """Update application status."""
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
