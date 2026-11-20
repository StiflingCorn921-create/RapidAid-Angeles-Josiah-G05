from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .forms import IncidentReportForm
from .models import IncidentReport


class IncidentListView(LoginRequiredMixin, ListView):
    model = IncidentReport
    template_name = "incidents/incident_list.html"
    context_object_name = "incidents"

    def get_queryset(self):
        return IncidentReport.objects.filter(reporter=self.request.user).select_related("category", "reporter")


class IncidentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = IncidentReport
    template_name = "incidents/incident_detail.html"
    context_object_name = "incident"

    def test_func(self):
        return self.get_object().reporter == self.request.user


class IncidentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = IncidentReport
    form_class = IncidentReportForm
    template_name = "incidents/incident_form.html"
    success_url = reverse_lazy("incident_list")
    success_message = "Incident report submitted successfully."

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)


class IncidentUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = IncidentReport
    form_class = IncidentReportForm
    template_name = "incidents/incident_form.html"
    success_url = reverse_lazy("incident_list")
    success_message = "Incident report updated successfully."

    def test_func(self):
        return self.get_object().reporter == self.request.user


class IncidentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = IncidentReport
    template_name = "incidents/incident_confirm_delete.html"
    context_object_name = "incident"
    success_url = reverse_lazy("incident_list")

    def test_func(self):
        return self.get_object().reporter == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Incident report deleted.")
        return super().form_valid(form)
