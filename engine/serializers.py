from rest_framework import serializers

from engine.models import Action, Step, Workflow

class WorkflowCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, allow_blank=True)
    name_ar = serializers.CharField(required=False, allow_blank=True)
    name_en = serializers.CharField(required=False, allow_blank=True)

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


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "name_ar", "name_en", "is_external", "step","next_step"]
