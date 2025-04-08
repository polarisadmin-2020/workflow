"""URLs for the configurations app."""

from django.urls import path

from .views import ApplicationStatusView

urlpatterns = [
    path(
        "application/<str:application_number>/status/", ApplicationStatusView.as_view()
    ),
]
