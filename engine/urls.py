from django.urls import path

from .views import StepCreateView, WorkflowCreateView

urlpatterns = [
    # Workflow endpoints
    path("workflows/create/", WorkflowCreateView.as_view(), name="workflow-create"),
    # Step endpoints
    path("steps/create/", StepCreateView.as_view(), name="step-create"),
]
