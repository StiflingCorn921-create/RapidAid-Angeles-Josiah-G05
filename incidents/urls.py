from django.urls import path
from .views import (
    IncidentCreateView,
    IncidentDeleteView,
    IncidentDetailView,
    IncidentListView,
    IncidentStatusUpdateView,
    IncidentUpdateView,
)

urlpatterns = [
    path("", IncidentListView.as_view(), name="incident_list"),
    path("new/", IncidentCreateView.as_view(), name="incident_create"),
    path("<int:pk>/", IncidentDetailView.as_view(), name="incident_detail"),
    path("<int:pk>/edit/", IncidentUpdateView.as_view(), name="incident_update"),
    path("<int:pk>/delete/", IncidentDeleteView.as_view(), name="incident_delete"),
    path("<int:pk>/status/", IncidentStatusUpdateView.as_view(), name="incident_status"),
]
