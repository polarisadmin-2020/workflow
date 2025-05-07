"""This file contains the views for the organizational_structure app."""

from rest_framework import generics

from organizational_structure.models import Position
from organizational_structure.serializers import PositionSerializer


class PositionListAPIView(generics.ListAPIView):
    """View to retrieve all positions."""

    queryset = Position.objects.all()
    serializer_class = PositionSerializer
