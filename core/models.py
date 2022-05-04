from django.db import models
from django.urls import reverse
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from datetime import datetime
from taggit.managers import TaggableManager
from bs4 import BeautifulSoup


class CauseManager(models.Manager):
    def get_queryset(self):
        return super(CauseManager, self).get_queryset().filter(active=True)


AVG_SPEED = 250


class Causes(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    # auto_now_add, add the time we saved initially
    updated = models.DateTimeField(auto_now=True)
    tags = TaggableManager(help_text='Select any of the tags related to the cause')
    sign_count = models.PositiveIntegerField(default=0)
    '''
    sign_count will be updated everytime a voteforcause is saved, so that I can know the number 
    of signature added for each cause.'''
    reading_time = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    published = CauseManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-id",)
        verbose_name_plural = "Causes"

    def get_absolute_url(self):
        return reverse("cause_detail", args=[self.slug])


@receiver(pre_save, sender=Causes)

def create_slug_field(sender, instance, **kwargs):
    '''To be run everytime before a save method is called on Cause, it will set the calculated value
    of the reading time
    '''
    obj = BeautifulSoup(instance.body, 'html.parser')
    obj_len = len(obj.text.split(' '))
    instance.reading_time = obj_len / AVG_SPEED
    # instance.reading_time =


class VoteForCause(models.Model):
    cause = models.ForeignKey(Causes, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    has_signed = models.BooleanField(default=False)

    def __str__(self):
        return f'{str(self.cause)}'

    @property
    def time_diff(self):
        time = datetime.now()
        if self.timestamp.day == time.day:
            return str(time.hour - self.timestamp.hour) + " hours ago"
        else:
            if self.timestamp.month == time.month:
                return str(time.day - self.timestamp.day) + " days ago"
            else:
                if self.timestamp.year == time.year:
                    return str(time.month - self.timestamp.month) + " months ago"
        return self.timestamp

    class Meta:
        unique_together = ['cause', 'user']


@receiver(post_save, sender=VoteForCause)
def cause_sign_count_increment(sender, instance, created, **kwargs):
    '''
    The signal that will be runned after a user has voted for a particular cause, it will run on
    the causes itself, so as to increment the value of sign_count in the Causes.
    '''
    if created:
        instance.cause.sign_count += 1
        instance.cause.save()
