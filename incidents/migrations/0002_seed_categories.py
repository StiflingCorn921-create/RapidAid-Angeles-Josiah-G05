from django.db import migrations


def seed_categories(apps, schema_editor):
    EmergencyCategory = apps.get_model("incidents", "EmergencyCategory")
    defaults = [
        ("Cardiac Arrest", "Unresponsive person not breathing normally; requires CPR / AED."),
        ("Choking", "Airway obstruction preventing normal breathing or speaking."),
        ("Seizure", "Sudden uncontrolled electrical disturbance in the brain."),
        ("Severe Bleeding", "Heavy external blood loss requiring immediate pressure."),
    ]
    for name, description in defaults:
        EmergencyCategory.objects.get_or_create(name=name, defaults={"description": description})


def reverse_seed(apps, schema_editor):
    EmergencyCategory = apps.get_model("incidents", "EmergencyCategory")
    EmergencyCategory.objects.filter(
        name__in=["Cardiac Arrest", "Choking", "Seizure", "Severe Bleeding"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("incidents", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_seed),
    ]
