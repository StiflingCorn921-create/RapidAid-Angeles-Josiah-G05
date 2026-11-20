from django import forms
from .models import EmergencyCategory, IncidentReport


class IncidentReportForm(forms.ModelForm):
    category_name = forms.CharField(
        max_length=100,
        label="Category",
        widget=forms.TextInput(
            attrs={"class": "form-select", "list": "category-options", "autocomplete": "off"}
        ),
    )

    field_order = ("category_name", "title", "location", "severity", "description")

    class Meta:
        model = IncidentReport
        fields = ("title", "location", "severity", "description")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "severity": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe symptoms and immediate situation...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.category_id:
            self.fields["category_name"].initial = self.instance.category.name

    def clean_category_name(self):
        name = self.cleaned_data.get("category_name", "").strip()
        if len(name) < 2:
            raise forms.ValidationError("Please select or enter a valid category.")
        return name

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        category_name = self.cleaned_data["category_name"]
        existing = EmergencyCategory.objects.filter(name__iexact=category_name).first()
        if existing:
            instance.category = existing
        else:
            instance.category = EmergencyCategory.objects.create(name=category_name)

        if commit:
            instance.save()
        return instance


class IncidentStatusForm(forms.ModelForm):
    class Meta:
        model = IncidentReport
        fields = ("status",)
        widgets = {
            "status": forms.Select(attrs={"class": "form-select form-select-sm"}),
        }
