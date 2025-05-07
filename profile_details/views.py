"""This file contains the views for the profile details app."""

from rest_framework.generics import RetrieveAPIView

from profile_details.models import Employee
from profile_details.serializers import EmployeeSerializer


class EmployeeRetrieveView(RetrieveAPIView):
    """Retrieve and update Employee."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "employment_number"
