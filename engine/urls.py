from django.urls import path

from engine.views import StepCreateView, StepDeleteView, StepUpdateView, StepsByWorkflowView, WorkflowCreateView, WorkflowUpdateView

urlpatterns = [
    # Workflow endpoints
    path('workflows/create/', WorkflowCreateView.as_view(), name='workflow-create'),
    path('workflows/<int:pk>/update/', WorkflowUpdateView.as_view(), name='workflow-update'),

    # Step endpoints
    path('steps/create/', StepCreateView.as_view(), name='step-create'),
    path('steps/<int:pk>/update/', StepUpdateView.as_view(), name='step-update'),
    path('steps/<int:pk>/delete/', StepDeleteView.as_view(), name='step-delete'),
    path('workflows/<int:workflow_id>/steps/', StepsByWorkflowView.as_view(), name='workflow-steps'),
]
