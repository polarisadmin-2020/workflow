from django.urls import path

from engine.views import (
    ActionCreateView,
    ActionDeleteView,
    ActionListView,
    ActionUpdateView,
    StepCreateView,
    StepDeleteView,
    StepsByWorkflowView,
    StepUpdateView,
    WorkflowCreateView,
    WorkflowDeleteView,
    WorkflowListView,
    WorkflowUpdateView,
    StepsByApplicationView,
    CurrentStepByApplicationView,
)

urlpatterns = [
    # Workflow endpoints
    path("workflows/", WorkflowListView.as_view(), name="workflow_list"),
    path("workflows/create/", WorkflowCreateView.as_view(), name="workflow_create"),
    path(
        "workflows/<int:pk>/update/",
        WorkflowUpdateView.as_view(),
        name="workflow_update",
    ),
    path(
        "workflows/<int:pk>/delete/",
        WorkflowDeleteView.as_view(),
        name="workflow_delete",
    ),
    # Step endpoints
    path("steps/create/", StepCreateView.as_view(), name="step_create"),
    path("steps/<int:pk>/update/", StepUpdateView.as_view(), name="step_update"),
    path("steps/<int:pk>/delete/", StepDeleteView.as_view(), name="step_delete"),
    path(
        "workflows/<int:workflow_id>/steps/",
        StepsByWorkflowView.as_view(),
        name="workflow-steps",
    ),
    # Action endpoints
    path("actions/create/", ActionCreateView.as_view(), name="action_create"),
    path("actions/<int:pk>/update/", ActionUpdateView.as_view(), name="action_update"),
    path("actions/<int:pk>/delete/", ActionDeleteView.as_view(), name="action_delete"),
    path("actions/list/<int:step_id>/", ActionListView.as_view(), name="action_list"),
    # Application endpoints
    path("applications/<int:application_id>/steps/", StepsByApplicationView.as_view(), name="steps-by-application"),
    path("applications/<int:application_id>/current-step/", CurrentStepByApplicationView.as_view(), name="current-step-by-application"),
]
