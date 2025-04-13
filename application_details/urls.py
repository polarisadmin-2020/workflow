"""URLs for the configurations app."""

from django.urls import path

from .views import ApplicationRetrieveUpdateAPIView, ApplicationListView

urlpatterns = [
    path(
        "application/<str:application_number>/status/", 
        ApplicationRetrieveUpdateAPIView.as_view(),
    ),
    path("list/", ApplicationListView.as_view(), name="application-list",),
]
