from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


class CustomAdmin(UserAdmin):
    form = CustomUserChangeForm

    add_form = CustomUserCreationForm
    model = CustomUser


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone_number", "nationality"]


admin.site.register(CustomUser, CustomAdmin)
admin.site.register(Profile, ProfileAdmin)
