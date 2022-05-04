from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django_countries.fields import CountryField


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    nationality = CountryField()

    def __str__(self):
        return str(self.user) + " Profile"

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Profile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # add this
def create_user_profile(sender, instance, created, **kwargs):
    '''This signal will be run after saving a new user, its job is to create a profile for
    such a user.'''
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)

def save_user_profile(sender, instance, **kwargs):
    '''
    save the profile created by the signal above
    '''
    instance.profile.save()
