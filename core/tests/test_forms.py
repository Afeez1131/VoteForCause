from django.test import TestCase, SimpleTestCase
from core.models import Causes
from django.contrib.auth import get_user_model
from core.forms import CauseCreateForm, CauseUpdateForm


class CauseForms(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testing",
            password="secret",
            email="test@gmail.com",
        )

        self.cause = Causes.objects.create(
            author=self.user, title="New Cause", body="new cause " "description."
        )

    def test_cause_create_form(self):
        form_data = {
            # "author": self.user,
            "title": "New Cause Title",
            "body": "New Cause Body",
            "tags": ['Education', 'Racism']
        }
        form = CauseCreateForm(data=form_data)
        tag = form_data.get("tags")
        print('Tag ', form.cleaned_data["tags"])
        # self.assertEqual(response.status_code, 200)
        self.assertTrue(form.is_valid())
        # self.assertEqual(form.cleaned_data["author"], self.user)
        self.assertEqual(form.cleaned_data["title"], "New Cause Title")
        self.assertEqual(form.cleaned_data["body"], "New Cause Body")
        # self.assertListEqual(form.cleaned_data["tags"], tag)
        # print(form.__dict__)  will list all field methods just like in class
        # print(form.cleaned_data['author'])

    def test_cause_update_form(self):
        cause = Causes.objects.get(id=1)
        form = CauseUpdateForm(instance=cause)
        # self.assertTrue(form.is_valid())
        # self.assertEqual(form.initial.get("author"), self.user.id)
        self.assertEqual(form.initial.get("title"), "New Cause")
        self.assertEqual(form.initial.get("body"), "new cause " "description.")
        # print(form.clean().get('title'))
        # print(form.cleaned_data['author'])
