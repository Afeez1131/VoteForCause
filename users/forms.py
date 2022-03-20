from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from allauth.account.forms import LoginForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields
        # it has a single field which is the username, django handles the password field itself


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields
        # displays all the fields in the model, excluding the password field

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields["login"].label = ""
        self.fields["login"].widget.attrs[
            "placeholder"
        ] = "Enter your username or phone number"
        self.fields["login"].widget.attrs["class"] = "form-control"

        self.fields["password"].widget = forms.PasswordInput()
        self.fields["password"].widget.attrs[
            "placeholder"
        ] = "Enter your password..."
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].label = ""
