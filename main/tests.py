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
        self.assertContains(response, 'data-experiences-url="/api/v1/experiences/"')

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
        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = date(2024, 6, 1)
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

        response = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(response.status_code, 200)
        experience_data = response.json()[0]
        self.assertEqual(experience_data["title"], self.experience.title)
        self.assertEqual(experience_data["ended_at"], "Jun 2024")

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


from datetime import date
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient, APITestCase


class PortfolioAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse('api:experience-list')
        self.project_url = reverse('api:project-list')
        self.owner = User.objects.create_superuser('owner', 'owner@example.com', 'pass')
        self.editor = User.objects.create_user('editor', password='pass')
        self.editor.groups.add(Group.objects.create(name='Editor'))
        self.reader = User.objects.create_user('reader', password='pass')
        self.experience = Experience.objects.create(
            title='Existing role', organization='Lab', category='research',
            started_at=date(2024, 1, 1),
        )
        self.project = Project.objects.create(name='Existing project')
        self.experience_payload = {
            'title': 'New role', 'organization': 'Institute', 'description': 'Research',
            'category': 'research', 'started_at': '2025-01-01', 'ended_at': None,
        }

    def test_guest_and_regular_user_cannot_write_experiences(self):
        before = Experience.objects.count()
        self.assertEqual(self.client.post(self.list_url, self.experience_payload, format='json').status_code, 403)
        self.assertEqual(Experience.objects.count(), before)
        self.client.force_authenticate(self.reader)
        self.assertEqual(self.client.post(self.list_url, self.experience_payload, format='json').status_code, 403)
        self.assertEqual(Experience.objects.count(), before)
        self.assertEqual(self.client.patch(reverse('api:experience-detail', args=[self.experience.pk]), {'title': 'Hacked'}).status_code, 403)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, 'Existing role')

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        detail = reverse('api:experience-detail', args=[self.experience.pk])
        before = Experience.objects.count()
        self.assertEqual(self.client.post(self.list_url, self.experience_payload, format='json').status_code, 403)
        self.assertEqual(Experience.objects.count(), before)
        self.assertEqual(self.client.patch(detail, {'title': 'Edited by editor'}).status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, 'Edited by editor')
        self.assertEqual(self.client.delete(detail).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_owner_can_create_and_delete_experiences(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.experience_payload, format='json')
        self.assertEqual(response.status_code, 201)
        created_id = response.data['id']
        self.assertTrue(Experience.objects.filter(pk=created_id, title='New role').exists())
        self.assertEqual(self.client.delete(reverse('api:experience-detail', args=[created_id])).status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=created_id).exists())

    def test_invalid_experience_input_returns_400_without_saving(self):
        self.client.force_authenticate(self.owner)
        before = Experience.objects.count()
        invalid = {**self.experience_payload, 'ended_at': '2024-01-01'}
        response = self.client.post(self.list_url, invalid, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('ended_at', response.data)
        self.assertEqual(Experience.objects.count(), before)

    def test_star_requires_login_and_uses_authenticated_user(self):
        star_url = reverse('api:project-star', args=[self.project.pk])
        self.assertEqual(self.client.post(star_url).status_code, 403)
        self.assertFalse(self.project.starred_by.exists())
        self.client.force_authenticate(self.reader)
        self.assertEqual(self.client.post(star_url).status_code, 200)
        self.assertQuerySetEqual(self.project.starred_by.all(), [self.reader], transform=lambda user: user)

    def test_session_write_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='owner', password='pass')
        response = client.post(self.list_url, self.experience_payload, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
