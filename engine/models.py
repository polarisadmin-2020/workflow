from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from mongoengine import PULL, BooleanField, DictField, Document, StringField

from organizational_structure.models import Position


# Create your models here.
class Workflow(models.Model):
    code = models.PositiveIntegerField(null=True, blank=True)
    name_ar = models.CharField(max_length=255, blank=True, null=True)
    name_en = models.CharField(max_length=255, blank=True, null=True)
    subservice_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_en


class Step(models.Model):
    workflow = models.ForeignKey(
        Workflow, related_name="steps", on_delete=models.CASCADE
    )
    name_ar = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    position = models.ForeignKey(
        Position, related_name="Step", blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name_en

    form_id = models.CharField(max_length=255, blank=True, null=True)


class DynamicForm(Document):
    """Model to store dynamic forms received as JSON from the frontend."""

    name_en = StringField(required=True, max_length=255)  # Optional identifier
    name_ar = StringField(required=True, max_length=255)
    subservice_id = StringField(required=True, max_length=255)
    is_applicant_form = BooleanField(default=False)
    form_data = DictField(required=True)  # Stores the entire JSON data
    created_at = StringField(default=lambda: now().isoformat())  # Store timestamp

    meta = {
        "collection": "dynamic_forms",
        "indexes": [
            {
                "fields": ["subservice_id"],
                "unique": False,
            },
        ],
    }  # Define MongoDB collection name


class Action(models.Model):
    # Choices for action type
    ACTION_TYPE_CHOICES = [
        ('external_entity', _('External Entity')),
        ('complete_application', _('Complete Application')),
        ('step', _('Step')),
    ]
    
    # Choices for status
    STATUS_CHOICES = [
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('rejected', _('Rejected')),
    ]
    
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPE_CHOICES,
        default='step'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed'
    )
    step = models.ForeignKey(
        Step, on_delete=models.CASCADE, related_name="actions_from"
    )
    next_step = models.ForeignKey(
        Step, on_delete=models.CASCADE, related_name="actions_to"
    )

    def __str__(self):
        return self.name_en
