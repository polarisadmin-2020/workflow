"""This module defines various models for the Organizational structure."""

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext_lazy as _


class Position(Group):
    """DB Model to represent a Position."""

    arabic_name = models.CharField(
        max_length=200,
        verbose_name=_("Arabic Name"),
    )
    english_name = models.CharField(
        max_length=200,
        verbose_name=_("English Name"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Is Deleted"),
    )


    class Meta:
        """Metadata options for the Position model."""

        db_table = "position"
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")

    def __str__(self: "Position") -> str:
        """Return a human-readable string representation."""
        return f"{self.arabic_name} - {self.english_name}"
