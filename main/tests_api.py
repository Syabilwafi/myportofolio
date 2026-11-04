from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from main.models import Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", email="owner@example.com", password="test-password",
        )
        self.visitor = User.objects.create_user(
            username="visitor", password="test-password",
        )
        self.editor = User.objects.create_user(
            username="editor", password="test-password",
        )
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.project = Project.objects.create(
            name="Portfolio", description="My website", url="https://example.com/",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.pk])
        self.star_url = reverse("api:project-star", args=[self.project.pk])
        self.payload = {
            "name": "New project",
            "description": "A useful app",
            "url": "https://example.com/new-project/",
        }

    def test_public_list_and_detail_use_flat_serializer_data(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.pk))
        self.assertEqual(response.data[0]["name"], self.project.name)
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_missing_detail(self):
        self.assertEqual(len(self.client.get(self.list_url, {"q": "PORT"}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {"q": "website"}).data[0]["id"], str(self.project.pk))
        self.assertEqual(self.client.get(self.list_url, {"q": "missing"}).data, [])
        missing_url = reverse(
            "api:project-detail", args=["00000000-0000-0000-0000-000000000001"],
        )
        self.assertEqual(self.client.get(missing_url).status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project_url = reverse("api:project-detail", args=[response.data["id"]])
        response = self.client.patch(project_url, {"name": "Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated")
        self.assertEqual(self.client.delete(project_url).status_code, status.HTTP_204_NO_CONTENT)

    def test_visitor_cannot_write_and_editor_can_only_update(self):
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(
            self.client.post(self.list_url, self.payload, format="json").status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(
            self.client.patch(self.detail_url, {"name": "Edited"}, format="json").status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.client.delete(self.detail_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(
            self.client.post(self.star_url).status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.client.force_authenticate(user=self.visitor)
        self.assertTrue(self.client.post(self.star_url).data["is_starred"])
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_name_and_url_validation(self):
        self.client.force_authenticate(user=self.owner)
        for invalid_data, field in (
            ({"name": "   "}, "name"),
            ({"url": "javascript:alert(1)"}, "url"),
        ):
            response = self.client.post(
                self.list_url, {**self.payload, **invalid_data}, format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
