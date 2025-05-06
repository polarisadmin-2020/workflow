from rest_framework import serializers

from engine.models import Step, Workflow


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = [
            "id",
            "code",
            "name_ar",
            "name_en",
            "subservice_id",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ["id", "workflow", "name_ar", "name_en", "position", "form_id"]
