"""This file contains the serializers for the organizational_structure app."""

from rest_framework import serializers

from organizational_structure.models import Position


class PositionSerializer(serializers.ModelSerializer):
    """Used for retrieving and displaying data in a detailed format."""


    class Meta:
        """Metadata options for the PositionSerializer class."""

        model = Position
        fields = "__all__"
