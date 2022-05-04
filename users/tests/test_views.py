from django.test import TestCase, SimpleTestCase
from django.urls import reverse, reverse_lazy
from core.models import Causes
from django.contrib.auth import get_user_model
from django.test import Client
from django.conf import settings


class CauseTestView(TestCase):
    @classmethod
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            full_name="Test User",
            password="testpass123",
        )

        self.cause = Causes.objects.create(
            author=self.user, title="New Cause", body="new cause " "description."
        )

    def test_profile(self):
        """
        it requires a user to be logged in
        """
        credential = {"username": self.user.username, "password": "testpass123"}
        self.client.login(**credential)
        response = self.client.get(reverse("profile"))
        self.assertTemplateUsed(response, "profile.html")
        self.assertContains(response, "Profile")
