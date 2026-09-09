from datetime import date
from django.test import TestCase
from django.urls import reverse

from main.models import Experience


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Software Engineering Intern",
            organization="Tech Company",
            description="Working on backend systems.",
            category="internship",
            started_at=date(2024, 1, 1),
            ended_at=None,
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

        self.assertEqual(response.context["name"], "Syabil Wafi")
        self.assertEqual(response.context["npm"], "2506657371")

        self.assertContains(response, "Syabil")
        self.assertContains(response, self.experience.title)

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/non-existent-page/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model_methods(self):
        self.assertEqual(str(self.experience), "Software Engineering Intern at Tech Company")

        self.experience.organization = ""
        self.assertEqual(str(self.experience), "Software Engineering Intern")

        self.assertTrue(self.experience.is_ongoing)

        self.assertEqual(self.experience.get_category_display(), "Internship")

    def test_empty_experiences_state(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No experiences found.")

    def test_completed_experience(self):
        self.experience.ended_at = date(2024, 6, 1)
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

        response = self.client.get(reverse("main:show_main"))
        self.assertContains(response, "Jun 2024")
        self.assertNotContains(response, "Present")