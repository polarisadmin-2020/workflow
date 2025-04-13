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
class ApplicationRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """API view to get or update application status."""

    queryset = Application.objects
    serializer_class = DynamicApplicationSerializer

    def retrieve(self, request, *args, **kwargs):
        """Handle GET with 404 if application_number not found."""
        application_number = kwargs["application_number"]
        instance = Application.objects(application_number=application_number).first()

        if not instance:
            return Response(
                {"error": "Application not found"}, status=drf_status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Handle PATCH request to update application status
    def patch(self, request, application_number, *args, **kwargs):
        """Handle PATCH request ensuring 'application_number' is not sent."""
        application = Application.objects(application_number=application_number).first()

        if not application:
            return Response(
                {"error": "Application not found"}, status=drf_status.HTTP_404_NOT_FOUND
            )

        if "application_number" in request.data:
            return Response(
                {"error": "'application_number' cannot be edited."},
                status=drf_status.HTTP_400_BAD_REQUEST,
            )

        for key, value in request.data.items():
            if hasattr(application, key):
                setattr(application, key, value)
            else:
                print(f"Skipping unknown field: {key}")  # Optional debug

        application.save()
        application.reload()

        return Response(
            {
                "message": "Application status updated successfully",
                "Application number": str(application.application_number),
                "status": str(application.status),
            },
            status=drf_status.HTTP_200_OK,
        )
