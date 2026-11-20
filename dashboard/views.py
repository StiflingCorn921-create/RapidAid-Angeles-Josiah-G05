from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from accounts.models import CustomUser
from incidents.models import IncidentReport


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["role_display"] = user.get_role_display()
        context["is_admin"] = user.role == CustomUser.Role.ADMIN
        context["is_responder"] = user.role == CustomUser.Role.RESPONDER
        context["total_members"] = CustomUser.objects.count()
        context["my_incidents_count"] = IncidentReport.objects.filter(reporter=user).count()
        if user.role in [CustomUser.Role.RESPONDER, CustomUser.Role.ADMIN]:
            context["open_incidents_count"] = IncidentReport.objects.exclude(
                status=IncidentReport.Status.RESOLVED
            ).count()
        return context


class ResponderPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/responder.html"

    def test_func(self):
        user = self.request.user
        return user.role in [CustomUser.Role.RESPONDER, CustomUser.Role.ADMIN]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_incidents"] = (
            IncidentReport.objects.exclude(status=IncidentReport.Status.RESOLVED)
            .select_related("category", "reporter")[:10]
        )
        return context


class AdminPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/admin_panel.html"

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.Role.ADMIN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_incidents"] = IncidentReport.objects.count()
        context["open_incidents"] = IncidentReport.objects.filter(status=IncidentReport.Status.OPEN).count()
        context["resolved_incidents"] = IncidentReport.objects.filter(status=IncidentReport.Status.RESOLVED).count()
        return context
