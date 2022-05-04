from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    get_user_model,
    AuthenticationForm,
)
from allauth.account.forms import LoginForm, SignupForm, ChangePasswordForm
from users.models import Profile
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        models = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        models = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomRegistrationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        # self.fields["username"].widget.attrs["placeholder"] = "username..."
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].label = ""

        # self.fields["email"].widget.attrs["placeholder"] = "E-mail..."
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].label = ""
        self.fields["email"].widget.attrs["required"] = "required"

        # self.fields["password1"].widget.attrs["placeholder"] = "your password..."
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].label = ""

        # self.fields["password2"].widget.attrs["placeholder"] = "your password again..."
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].label = ""


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        # self.fields["login"].widget.attrs["placeholder"] = "username..."
        self.fields["login"].widget.attrs["class"] = "form-control"
        self.fields["login"].label = ""

        # self.fields["password"].widget.attrs["placeholder"] = "password..."
        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].label = ""


class CustomPasswordChange(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(CustomPasswordChange, self).__init__(*args, **kwargs)

        self.fields["oldpassword"].widget.attrs["placeholder"] = "current password ..."
        self.fields["oldpassword"].widget.attrs["class"] = "form-control"
        self.fields["oldpassword"].label = ""

        self.fields["password1"].widget.attrs["placeholder"] = "new password..."
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].label = ""

        self.fields["password2"].widget.attrs["placeholder"] = "new password again..."
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].label = ""


from allauth.account.forms import ResetPasswordForm


def CustomPasswordReset(ResetPasswordForm):
    email = forms.EmailField()


class ProfileForm(forms.ModelForm):
    country = CountryField(blank_label="(select country)")

    class Meta:
        model = Profile
        fields = ["phone_number", "nationality"]
        widgets = {"country": CountrySelectWidget()}

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # self.fields["password1"].widget.attrs["placeholder"] = "your password..."
        self.fields["phone_number"].widget.attrs["required"] = "required"
        # self.fields['phone_number'].label = ''

        # self.fields["password1"].widget.attrs["placeholder"] = "your password..."
        self.fields["nationality"].widget.attrs["required"] = "required"
        # self.fields['phone_number'].label = ''


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["required"] = "required"
        self.fields["last_name"].widget.attrs["required"] = "required"
        self.fields["email"].widget.attrs["required"] = "required"
