from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from .forms import CustomUserCreationForm, UserProfileUpdateForm


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = "Your RapidAid account was created successfully! Please log in."


class ProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Your profile details have been updated."

    def get_object(self, queryset=None):
        return self.request.user

