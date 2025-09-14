from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Count

from engine.models import Action, Step, Workflow
from engine.serializers import ActionSerializer, StepSerializer, WorkflowCreateSerializer, WorkflowSerializer
from application_details.models import Application


# Create your views here.
class WorkflowCreateView(generics.CreateAPIView):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowCreateSerializer


class WorkflowListView(generics.ListAPIView):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer


class WorkflowUpdateView(generics.UpdateAPIView):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    lookup_field = "pk"


class WorkflowDeleteView(generics.DestroyAPIView):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    lookup_field = "pk"


class StepsByWorkflowView(generics.ListAPIView):
    serializer_class = StepSerializer

    def get_queryset(self):
        workflow_id = self.kwargs["workflow_id"]
        return Step.objects.filter(workflow_id=workflow_id).annotate(
            action_count=Count('actions_from')
        ).order_by("id")


class StepCreateView(generics.CreateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class StepUpdateView(generics.UpdateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    lookup_field = "pk"


class StepDeleteView(generics.DestroyAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    lookup_field = "pk"


class ActionCreateView(generics.CreateAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


class ActionUpdateView(generics.UpdateAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    lookup_field = "pk"


class ActionDeleteView(generics.DestroyAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    lookup_field = "pk"


class ActionListView(generics.ListAPIView):
    serializer_class = ActionSerializer

    def get_queryset(self):
        step_id = self.kwargs["step_id"]
        return Action.objects.filter(step_id=step_id).order_by("id")


class StepsByApplicationView(generics.ListAPIView):
    """
    Return all steps for a given application_number.
    Gets the position from the application and returns steps for that position.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StepSerializer

    def get_queryset(self):
        application_number = self.kwargs["application_number"]
        
        # Get the application to find its position
        try:
            application = Application.objects.get(application_number=application_number)
            position_id = application.position_id
            
            if not position_id:
                return Step.objects.none()
                
            # Return steps for the position
            return Step.objects.filter(position_id=position_id).order_by("id")
        except Application.DoesNotExist:
            return Step.objects.none()


class CurrentStepByApplicationView(generics.RetrieveAPIView):
    """
    Return the latest step for a given application_number.
    Gets the position from the application and returns the latest step for that position.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StepSerializer

    def get_object(self):
        application_number = self.kwargs["application_number"]
        
        # Get the application to find its position
        try:
            application = Application.objects.get(application_number=application_number)
            position_id = application.position_id
            
            if not position_id:
                return None
                
            # Return the latest step for the position
            return Step.objects.filter(position_id=position_id).order_by("-id").first()
        except Application.DoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        """Handle GET with 404 if application or step not found."""
        instance = self.get_object()
        if instance is None:
            return Response(
                {"error": "Application not found or no steps available for this application's position"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
