"""This file contains the urls for the profile details app."""

from django.urls import path

from profile_details.views import EmployeeRetrieveView

urlpatterns = [
    path(
        "employees/<int:employment_number>/",
        EmployeeRetrieveView.as_view(),
        name="employee-detail",
    ),
]
