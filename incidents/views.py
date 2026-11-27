from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from accounts.models import CustomUser
from .forms import IncidentReportForm, IncidentStatusForm
from .models import EmergencyCategory, IncidentReport


def is_responder_or_admin(user):
    return user.role in [CustomUser.Role.RESPONDER, CustomUser.Role.ADMIN]


class IncidentObjectMixin:
    def get_object(self, queryset=None):
        return get_object_or_404(IncidentReport, pk=self.kwargs["pk"])


class IncidentListView(LoginRequiredMixin, ListView):
    model = IncidentReport
    template_name = "incidents/incident_list.html"
    context_object_name = "incidents"

    def get_queryset(self):
        qs = IncidentReport.objects.select_related("category", "reporter")
        if is_responder_or_admin(self.request.user):
            return qs
        return qs.filter(reporter=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_staff_role"] = is_responder_or_admin(self.request.user)
        return context


class IncidentDetailView(LoginRequiredMixin, IncidentObjectMixin, UserPassesTestMixin, DetailView):
    model = IncidentReport
    template_name = "incidents/incident_detail.html"
    context_object_name = "incident"

    def test_func(self):
        incident = self.get_object()
        return incident.reporter == self.request.user or is_responder_or_admin(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_staff_role"] = is_responder_or_admin(self.request.user)
        context["status_form"] = IncidentStatusForm(instance=self.object)
        return context


class IncidentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = IncidentReport
    form_class = IncidentReportForm
    template_name = "incidents/incident_form.html"
    success_url = reverse_lazy("incident_list")
    success_message = "Incident report submitted successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = EmergencyCategory.objects.all()
        return context

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class IncidentUpdateView(LoginRequiredMixin, IncidentObjectMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = IncidentReport
    form_class = IncidentReportForm
    template_name = "incidents/incident_form.html"
    success_url = reverse_lazy("incident_list")
    success_message = "Incident report updated successfully."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = EmergencyCategory.objects.all()
        return context

    def test_func(self):
        incident = self.get_object()
        if self.request.user.role == CustomUser.Role.ADMIN:
            return True
        return incident.reporter == self.request.user and incident.status != IncidentReport.Status.RESOLVED

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class IncidentDeleteView(LoginRequiredMixin, IncidentObjectMixin, UserPassesTestMixin, DeleteView):
    model = IncidentReport
    template_name = "incidents/incident_confirm_delete.html"
    context_object_name = "incident"
    success_url = reverse_lazy("incident_list")

    def test_func(self):
        incident = self.get_object()
        if self.request.user.role == CustomUser.Role.ADMIN:
            return True
        return incident.reporter == self.request.user and incident.status != IncidentReport.Status.RESOLVED

    def form_valid(self, form):
        messages.success(self.request, "Incident report deleted.")
        return super().form_valid(form)


class IncidentStatusUpdateView(LoginRequiredMixin, IncidentObjectMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = IncidentReport
    form_class = IncidentStatusForm
    http_method_names = ["post"]
    success_message = "Incident status updated."

    def test_func(self):
        return is_responder_or_admin(self.request.user)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid status selection.")
        return redirect("incident_detail", pk=self.object.pk)

    def get_success_url(self):
        return reverse("incident_detail", kwargs={"pk": self.object.pk})
