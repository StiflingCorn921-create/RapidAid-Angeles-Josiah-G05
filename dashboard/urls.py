from django.urls import path
from .views import DashboardView, ResponderPanelView, AdminPanelView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("responder/", ResponderPanelView.as_view(), name="responder_panel"),
    path("admin-panel/", AdminPanelView.as_view(), name="admin_panel"),
]
