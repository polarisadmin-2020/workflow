"""Configuration serializers."""

from typing import Any, Dict

from rest_framework_mongoengine.serializers import DocumentSerializer

from .models import Application


class ApplicationSerializer(DocumentSerializer):
    """Serializer for application_details."""

    class Meta:
        """Metadata options for the ApplicationSerializer class."""

        model = Application
        fields = "__all__"

    # application_number = serializers.CharField()
    # status = serializers.CharField()

    # def update(
    #     self,
    #     instance: Application,
    #     validated_data: Dict[str, Any],
    # ) -> Application:
    #     """Update application status."""
    #     instance.status = validated_data.get("status", instance.status)
    #     instance.save()
    #     return instance
