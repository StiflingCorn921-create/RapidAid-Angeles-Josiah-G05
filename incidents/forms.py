from django import forms
from .models import IncidentReport


class IncidentReportForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ("category", "title", "location", "severity", "description")
        widgets = {
            "category": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Person collapsed near Main Gate"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Building A, 2nd Floor Lobby"}),
            "severity": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe symptoms and immediate situation..."}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_location(self):
        location = self.cleaned_data.get("location", "").strip()
        if len(location) < 3:
            raise forms.ValidationError("Please provide a valid location.")
        return location
