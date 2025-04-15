"""This file contains the serializers for the profile details app."""

from rest_framework import serializers

from organizational_structure.serializers import PositionSerializer

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"
