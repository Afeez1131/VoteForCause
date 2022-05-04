from .models import Causes, VoteForCause
from django.contrib import admin


class CustomAdmin(admin.ModelAdmin):
    list_display = ("title", "created", 'slug', "updated", 'sign_count')


class CustomVoteForCause(admin.ModelAdmin):
    list_display = ['cause', 'user', 'has_signed']


admin.site.register(Causes, CustomAdmin)
admin.site.register(VoteForCause, CustomVoteForCause)
