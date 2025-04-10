"""URLs for the configurations app."""

from django.urls import path

from .views import ApplicationStatusView, ApplicationListView

urlpatterns = [
    path(
        "application/<str:application_number>/status/", 
        ApplicationStatusView.as_view(),
    ),
    path("list/", ApplicationListView.as_view(), name="application-list",),
]
