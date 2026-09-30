from datetime import date
from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Project


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

        self.project = Project.objects.create(
            name="Portfolio Website",
            description="Project Description",
            url="https://example.com",
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
        self.assertContains(response, "No experience found.")

    def test_completed_experience(self):
        self.experience.ended_at = date(2024, 6, 1)
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

        response = self.client.get(reverse("main:show_main"))
        self.assertContains(response, "Jun 2024")
        self.assertNotContains(response, "Present")

    def test_project_url_is_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_project_model_data_renders_correctly(self):
        self.assertEqual(str(self.project), "Portfolio Website")

        response = self.client.get(reverse("main:get_projects_json"))
        fields = response.json()[0]['fields']
        self.assertEqual(fields['name'], self.project.name)
        self.assertEqual(fields['description'], self.project.description)
        self.assertEqual(fields['url'], self.project.url)

    def test_empty_projects_state(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])


class ProjectAjaxTests(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.admin = User.objects.create_user('admin', is_superuser=True)
        self.user = User.objects.create_user('reader')
        self.url = reverse('main:create_project_ajax')
        self.payload = {'name': 'New project', 'url': 'https://example.com', 'description': 'Plain text'}

    def test_creation_requires_superuser(self):
        self.assertEqual(self.client.post(self.url, self.payload).status_code, 401)
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(self.url, self.payload).status_code, 403)
        self.assertFalse(Project.objects.exists())

    def test_valid_creation_and_method(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(pk=response.json()['id'], name='New project').exists())

    def test_invalid_input_is_not_saved(self):
        self.client.force_login(self.admin)
        for changes in ({'name': ''}, {'name': '<img src=x onerror=alert(1)>'},
                        {'description': '<script>alert(1)</script>'}, {'url': 'javascript:alert(1)'},
                        {'url': 'ftp://example.com'}):
            with self.subTest(changes=changes):
                response = self.client.post(self.url, {**self.payload, **changes})
                self.assertEqual(response.status_code, 400)
                self.assertIn('errors', response.json())
        self.assertFalse(Project.objects.exists())

    def test_csrf_is_required(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        self.assertEqual(client.post(self.url, self.payload).status_code, 403)
        client.get(reverse('main:show_main'))
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post(self.url, self.payload, HTTP_X_CSRFTOKEN=token).status_code, 201)

    def test_search_and_user_specific_stars(self):
        project = Project.objects.create(name='Portfolio', description='A & B < C')
        Project.objects.create(name='Other')
        project.starred_by.add(self.user)
        url = reverse('main:get_projects_json')
        self.client.force_login(self.user)
        response = self.client.get(url, {'name': '  PORT  '})
        self.assertEqual(len(response.json()), 1)
        fields = response.json()[0]['fields']
        self.assertEqual(fields['stars_count'], 1)
        self.assertTrue(fields['is_starred'])
        self.client.logout()
        self.assertFalse(self.client.get(url, {'name': 'port'}).json()[0]['fields']['is_starred'])
