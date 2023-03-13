import os
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from team_meeting.models import Project, Team

PROJECT_URL = reverse("team-meeting:project-list")


def image_upload_url(project_id):
    """Return URL for image upload"""
    return reverse("team-meeting:project-upload-image", args=[project_id])


def create_sample_image(project, client):
    """Create and post sample image to the specific project instance"""
    url = image_upload_url(project.id)
    with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
        img = Image.new("RGB", (10, 10))
        img.save(ntf, format="JPEG")
        ntf.seek(0)
        res = client.post(url, {"image": ntf}, format="multipart")
    return res


class AuthenticatedImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.project = Project.objects.create(name="Taxi")
        self.team = Team.objects.create(
            name="Backend", project=self.project, num_of_members=7
        )

    def tearDown(self):
        self.project.image.delete()

    def test_upload_image_to_project(self):
        res = create_sample_image(self.project, self.client)
        self.project.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn("image", res.data)


class AdminImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.project = Project.objects.create(name="Taxi")
        self.team = Team.objects.create(
            name="Backend", project=self.project, num_of_members=7
        )

    def tearDown(self):
        self.project.image.delete()

    def test_upload_image_to_project(self):
        res = create_sample_image(self.project, self.client)
        self.project.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.project.image.path))

    def test_upload_image_bad_request(self):
        url = image_upload_url(self.project.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_project_list_should_not_work(self):
        url = PROJECT_URL
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {
                    "name": "Library",
                    "image": ntf,
                },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        project = Project.objects.get(name="Library")
        self.assertFalse(project.image)

    def test_image_url_is_shown_on_project_detail(self):
        create_sample_image(self.project, self.client)
        res = self.client.get(reverse("team-meeting:project-detail", args=[self.project.id]))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_project_list(self):
        create_sample_image(self.project, self.client)
        res = self.client.get(PROJECT_URL)

        self.assertIn("image", res.data[0].keys())

    def test_image_url_is_shown_on_team_detail(self):
        create_sample_image(self.project, self.client)
        res = self.client.get(reverse("team-meeting:team-detail", args=[self.team.id]))

        self.assertIn("image", res.data["project"].keys())
