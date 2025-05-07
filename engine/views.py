from rest_framework import generics

from engine.models import Step, Workflow
from engine.serializers import StepSerializer, WorkflowSerializer


# Create your views here.
class WorkflowCreateView(generics.CreateAPIView):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer


class WorkflowUpdateView(generics.UpdateAPIView):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    lookup_field = 'pk'



class StepsByWorkflowView(generics.ListAPIView):
    serializer_class = StepSerializer

    def get_queryset(self):
        workflow_id = self.kwargs['workflow_id']
        return Step.objects.filter(workflow_id=workflow_id).order_by('id')


class StepCreateView(generics.CreateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer


class StepUpdateView(generics.UpdateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    lookup_field = 'pk'


class StepDeleteView(generics.DestroyAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
    lookup_field = 'pk'