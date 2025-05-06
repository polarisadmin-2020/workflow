from rest_framework import generics

from engine.models import Step, Workflow
from engine.serializers import StepSerializer, WorkflowSerializer


# Create your views here.
class WorkflowCreateView(generics.CreateAPIView):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer


class StepCreateView(generics.CreateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
