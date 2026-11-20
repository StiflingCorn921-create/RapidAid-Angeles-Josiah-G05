from django.contrib import admin
from .models import EmergencyCategory, IncidentReport


@admin.register(EmergencyCategory)
class EmergencyCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "reporter", "severity", "status", "created_at"]
    list_filter = ["status", "severity", "category"]
    search_fields = ["title", "location", "reporter__username"]
