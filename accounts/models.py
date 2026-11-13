from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        BYSTANDER = "BYSTANDER", "Bystander / General Public"
        RESPONDER = "RESPONDER", "Certified First Responder"
        ADMIN = "ADMIN", "System Administrator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.BYSTANDER,
        help_text="User system access role"
    )
    phone_number = models.CharField(max_length=20, blank=True, help_text="Emergency contact phone number")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
