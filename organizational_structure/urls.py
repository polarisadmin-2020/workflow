"""This file contains the URL configuration for the organizational_structure app."""

from django.urls import path

from organizational_structure.views import PositionListAPIView

urlpatterns = [
    path(
        "positions/",
        PositionListAPIView.as_view(),
        name="position-list",
    ),
]
