from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from .models import EmergencyCategory, IncidentReport

User = get_user_model()


class IncidentCoreFeatureTests(TestCase):
    def setUp(self):
        self.bystander1 = User.objects.create_user(
            username="bystander1",
            email="b1@example.com",
            password="StrongPassword123!",
            role=User.Role.BYSTANDER,
        )
        self.bystander2 = User.objects.create_user(
            username="bystander2",
            email="b2@example.com",
            password="StrongPassword123!",
            role=User.Role.BYSTANDER,
        )
        self.responder = User.objects.create_user(
            username="responder1",
            email="r1@example.com",
            password="StrongPassword123!",
            role=User.Role.RESPONDER,
        )
        self.category, _ = EmergencyCategory.objects.get_or_create(name="Cardiac Arrest")
        self.incident_b1 = IncidentReport.objects.create(
            reporter=self.bystander1,
            category=self.category,
            title="Collapsed near main gate",
            location="Main Gate Lobby",
            severity=IncidentReport.Severity.HIGH,
            description="Unresponsive adult, needs immediate check.",
        )

    def test_login_required_for_incident_list(self):
        response = self.client.get(reverse("incident_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_login_required_for_incident_create(self):
        response = self.client.post(
            reverse("incident_create"),
            {
                "category_name": "Cardiac Arrest",
                "title": "Anonymous test report",
                "location": "Hallway",
                "severity": "MEDIUM",
                "description": "Should not save.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(IncidentReport.objects.count(), 1)

    def test_create_incident_valid_existing_category(self):
        self.client.force_login(self.bystander1)
        response = self.client.post(
            reverse("incident_create"),
            {
                "category_name": "Cardiac Arrest",
                "title": "Person fainted at gym",
                "location": "Campus Gym",
                "severity": "HIGH",
                "description": "Breathing shallowly, needs assistance.",
            },
        )
        self.assertRedirects(response, reverse("incident_list"))
        self.assertEqual(IncidentReport.objects.count(), 2)

    def test_create_incident_valid_custom_category(self):
        self.client.force_login(self.bystander1)
        response = self.client.post(
            reverse("incident_create"),
            {
                "category_name": "Heat Stroke",
                "title": "Runner dizzy on track",
                "location": "Oval Field",
                "severity": "MEDIUM",
                "description": "Overheated and disoriented.",
            },
        )
        self.assertRedirects(response, reverse("incident_list"))
        self.assertTrue(EmergencyCategory.objects.filter(name="Heat Stroke").exists())
        self.assertEqual(IncidentReport.objects.count(), 2)

    def test_create_incident_invalid_input(self):
        self.client.force_login(self.bystander1)
        response = self.client.post(
            reverse("incident_create"),
            {
                "category_name": "Cardiac Arrest",
                "title": "Hi",
                "location": "A",
                "severity": "MEDIUM",
                "description": "",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(IncidentReport.objects.count(), 1)
        self.assertContains(response, "Title must be at least 5 characters long.")

    def test_bystander_blocked_from_other_users_record(self):
        self.client.force_login(self.bystander2)
        for url_name in ("incident_detail", "incident_update", "incident_delete"):
            response = self.client.get(reverse(url_name, kwargs={"pk": self.incident_b1.pk}))
            self.assertEqual(response.status_code, 403)

    def test_bystander_cannot_edit_resolved_incident(self):
        self.incident_b1.status = IncidentReport.Status.RESOLVED
        self.incident_b1.save()
        self.client.force_login(self.bystander1)
        edit_res = self.client.get(reverse("incident_update", kwargs={"pk": self.incident_b1.pk}))
        del_res = self.client.get(reverse("incident_delete", kwargs={"pk": self.incident_b1.pk}))
        self.assertEqual(edit_res.status_code, 403)
        self.assertEqual(del_res.status_code, 403)

    def test_responder_can_view_all_and_update_status(self):
        self.client.force_login(self.bystander1)
        bystander_post = self.client.post(
            reverse("incident_status", kwargs={"pk": self.incident_b1.pk}),
            {"status": IncidentReport.Status.IN_PROGRESS},
        )
        self.assertEqual(bystander_post.status_code, 403)

        self.client.force_login(self.responder)
        list_res = self.client.get(reverse("incident_list"))
        self.assertContains(list_res, self.incident_b1.title)

        status_res = self.client.post(
            reverse("incident_status", kwargs={"pk": self.incident_b1.pk}),
            {"status": IncidentReport.Status.IN_PROGRESS},
        )
        self.assertRedirects(status_res, reverse("incident_detail", kwargs={"pk": self.incident_b1.pk}))
        self.incident_b1.refresh_from_db()
        self.assertEqual(self.incident_b1.status, IncidentReport.Status.IN_PROGRESS)

    def test_invalid_incident_id_returns_404(self):
        self.client.force_login(self.bystander1)
        response = self.client.get(reverse("incident_detail", kwargs={"pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_category_in_use_protected_from_delete(self):
        with self.assertRaises(ProtectedError):
            self.category.delete()
