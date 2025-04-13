"""Views for managing application status."""

from typing import Any, Dict

from rest_framework import status as drf_status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application
from .serializers import DynamicApplicationSerializer


class ApplicationListView(generics.ListAPIView):
    """View to list all Applications."""

    queryset = Application.objects
    serializer_class = DynamicApplicationSerializer
    

# API view to retrieve and update application status
class ApplicationStatusView(APIView):
    """API view to get or update application status."""

    def get(self, request: "Request", application_number: str) -> Response:
        """Return the status of an application by its application number."""

        try:
            application = Application.objects.get(application_number=application_number)
            serializer = DynamicApplicationSerializer(application)
            return Response(serializer.data)
        except Application.DoesNotExist:
            return Response(
                {"error": "Application not found"}, status=drf_status.HTTP_404_NOT_FOUND
            )

    # Handle PATCH request to update application status
    def patch(self, request: Request, application_number: str) -> Response:
        """Update the status of an application by its application number."""

        try:
            application = Application.objects.get(application_number=application_number)
        except Application.DoesNotExist:
            return Response(
                {"error": "Application not found"}, status=drf_status.HTTP_404_NOT_FOUND
            )

        serializer = DynamicApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)
