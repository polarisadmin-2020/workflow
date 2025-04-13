"""This file contains the URL configuration for the login app."""

from django.urls import path

from .views import login_view

urlpatterns = [
    path(
        "",
        login_view,
        name="login",
    ),
]
