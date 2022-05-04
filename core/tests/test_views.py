from django.test import TestCase, SimpleTestCase
from django.urls import reverse, reverse_lazy
from core.models import Causes
from users.models import Profile
from django.contrib.auth import get_user_model
from django.test import Client
from django.conf import settings


class CauseTestView(TestCase):
    @classmethod
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass123",
        )

        # self.profile = Profile.objects.get(user=self.user)
        # self.profile.phone_number = '08105506074'
        # self.profile.nationality = 'Nigeria'
        # self.profile.save()

        self.user.profile.phone_number = '08105506074'
        self.user.profile.nationality = 'Nigeria'
        self.user.save()

        self.cause = Causes.objects.create(
            author=self.user, title="New Cause", slug='new-cause', body="new cause " "description."
        )
        # i need to pass a custom slug so i can use get_absolute-url

    def test_homepage_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "causes_list.html")
        self.assertTemplateNotUsed(response, "unused_template.html")

    def test_homepage_url_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "causes_list.html")

    def test_cause_detail_view(self):
        response = self.client.get(self.cause.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cause_detail.html")
        self.assertContains(response, "Share")
        self.assertContains(response, "new cause description")
        self.assertNotContains(response, "Add New Cause")

    def test_cause_create_view(self):
        """
        requires for a user to be logged in before he can create a cause.
        before a user can create a cause, the user shoulsd have editer its profile to provide
        phone number and nationality
        # """

        c = Client()
        # c.login(username=self.user.username, password=self.user.password)
        c.force_login(user=self.user)
        # # since i only need concern myself about being logged in, then use force_login
        response = c.get(reverse_lazy("create_cause"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cause_create.html")
        self.assertContains(response, "Create Cause")

    def test_not_updated_profile_create_cause(self):
        '''
        testing if we try creating cause with an un-updated profile this should redirect to the
        edit profile page
        '''
        c = Client()
        fake_user = get_user_model().objects.create_user(username='fake_user',
                                                         email='fake_email.com',
                                                         password='password')
        c.force_login(fake_user)
        response = c.get(reverse('create_cause'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        # self.assertContains(response, 'Edit')

    def test_cause_update_view(self):
        """
        for a user to update a cause, the cause should be created by that user
        or raise permissiondenied exception
        """
        c = Client()
        c.force_login(user=self.user)
        response = c.get(reverse_lazy("update_cause", args=[self.cause.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cause_update.html")
        self.assertContains(response, "Update Cause")
        self.assertNotContains(response, "text not in response")
        self.assertNotContains(response, "Add New Cause")

    def test_cause_update_view(self):
        """
        for a user to edit a cause, the cause should be created by that user
        or raise permission denied exception, and here i am trying a fake user, so 403 (
        permission denied exception) as expected.
        """
        c = Client()
        fake_user = get_user_model().objects.create_user(username='fake_user',
                                                         email='fake_email.com',
                                                         password='password')
        c.force_login(fake_user)
        response = c.get(reverse_lazy("update_cause", args=[self.cause.slug]))
        self.assertEqual(response.status_code, 403)
        # self.assertTemplateUsed(response, "cause_update.html")
        # self.assertContains(response, "Update Cause")
        # self.assertNotContains(response, "text not in response")
        # self.assertNotContains(response, "Add New Cause")
