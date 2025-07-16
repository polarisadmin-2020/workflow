from rest_framework import generics

from engine.models import Action, Step, Workflow
from engine.serializers import ActionSerializer, StepSerializer, WorkflowCreateSerializer, WorkflowSerializer


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
        return Step.objects.filter(workflow_id=workflow_id).order_by("id")


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
