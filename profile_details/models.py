"""This module defines various models for the Organizational structure."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from organizational_structure.models import Position


class Employee(AbstractUser):
    """DB Model to represent an Employee."""

    username = None
    groups = None
    user_permissions = None
    employment_number = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Employment Number"),
    )
    second_name = models.CharField(
        max_length=200,
        verbose_name=_("Second Number"),
        null=True,
        blank=True,
    )
    Third_name = models.CharField(
        max_length=200,
        verbose_name=_("Third Number"),
        null=True,
        blank=True,
    )
    job_title = models.CharField(
        max_length=200,
        verbose_name=_("Job Title"),
    )
    mobile_number = models.CharField(
        max_length=200,
        verbose_name=_("Mobile Number"),
    )
    email = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("Email"),
    )
    address = models.CharField(
        max_length=500,
        verbose_name=_("Address"),
    )
    password = models.CharField(
        max_length=128,
        default="P@ssw0rd",
        verbose_name=_("Password"),
    )
    positions = models.ManyToManyField(
        Position,
        related_name="employees",
        verbose_name=_("Positions"),
        blank=True,
    )
    profile_image = models.ImageField(
        upload_to="employee_images/",
        verbose_name=_("Profile Image"),
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "employment_number"

    class Meta:
        """Metadata options for the Employee model."""

        db_table = "employees"
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self: "Employee") -> str:
        """Returns a string representation of the object."""
        return self.get_full_name()
