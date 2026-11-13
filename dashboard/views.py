from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from accounts.models import CustomUser


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["role_display"] = user.get_role_display()
        context["is_admin"] = user.role == CustomUser.Role.ADMIN
        context["is_responder"] = user.role == CustomUser.Role.RESPONDER
        context["total_members"] = CustomUser.objects.count()
        return context


class ResponderPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/responder.html"

    def test_func(self):
        user = self.request.user
        return user.role in [CustomUser.Role.RESPONDER, CustomUser.Role.ADMIN]


class AdminPanelView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/admin_panel.html"

    def test_func(self):
        user = self.request.user
        return user.role == CustomUser.Role.ADMIN

