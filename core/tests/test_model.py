from core.models import Causes, VoteForCause
from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModel(TestCase):
    @classmethod
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass123",
        )

        self.cause = Causes.objects.create(
            author=self.user, title="New Cause", body="new cause " "description."
        )

        self.vote = VoteForCause.objects.create(cause=self.cause, user=self.user)

    def test_custom_user(self):
        user = get_user_model().objects.get(id=1)
        self.assertEqual(self.user, user)
        self.assertEqual(self.user.username, user.username)
        self.assertEqual(self.user.email, user.email)

    def test_causes_model(self):
        self.assertEqual(self.cause.id, 1)
        self.assertEqual(self.cause.title, "New Cause")
        self.assertEqual(self.cause.body, "new cause description.")
        self.assertEqual(self.cause.author, self.user)

    def test_voteforcauses_model(self):
        self.assertEqual(self.vote.id, 1)
        self.assertEqual(self.vote.cause, self.cause)
        self.assertEqual(self.vote.user, self.user)
        self.assertEqual(self.vote.count, 1)
