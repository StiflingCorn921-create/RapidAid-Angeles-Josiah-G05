from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class EmergencyCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(2)])
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Emergency Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class IncidentReport(models.Model):
    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incident_reports",
    )
    category = models.ForeignKey(
        EmergencyCategory,
        on_delete=models.PROTECT,
        related_name="incidents",
    )
    title = models.CharField(max_length=150, validators=[MinLengthValidator(5)])
    location = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.MEDIUM,
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.OPEN,
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
