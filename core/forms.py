from django import forms
from .models import Causes
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
import re
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

TAG_CHOICES = (
    ('Racism', 'Racism'),
    ('Religion', 'Religion'),
    ('Education', 'Education'),
    ('Economy', 'Economy'),
    ('Environment', 'Environment'),
)


class CauseCreateForm(forms.ModelForm):
    class Meta:
        model = Causes
        fields = ("title", "body", 'tags', 'slug')
        widgets = {
            "body": SummernoteWidget(),
            'tags': forms.CheckboxSelectMultiple(choices=TAG_CHOICES),
            # convert the tags to a multi-select field with options of the Tag-choices declared
            # above
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super(CauseCreateForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget.attrs["placeholder"] = "Cause Title..."
        self.fields["title"].widget.attrs["class"] = "form-control"

    def clean_tags(self):
        '''
        The tags are not rendering well, therefore
        1. use regex to extract only words and not the symbols from the tag list
        2. convert the word into a list
        3. for each element in the list, strip out the spaces
        '''
        data = (self.cleaned_data['tags'])
        valid = re.sub(r'[^\w]', ' ', str(data))
        vd = valid.split(' ')
        delete_empty = [ele for ele in vd if ele.strip()]
        return delete_empty



    def clean_slug(self):
        '''
        This will get the slug from the title, try and see if a cause with the same slug exist
        If it exist, raise an inline form errors,
        else, assigned the slug to the new cause and return the slug
        '''
        title = self.cleaned_data['title']
        slug_title = slugify(title)
        cause = Causes.objects.filter(slug=slug_title)
        if cause.exists():
            raise ValidationError(f'Cause Title {title} exist, Change the title and Try again')
        return slug_title

class CauseUpdateForm(forms.ModelForm):
    class Meta:
        model = Causes
        fields = ("title", "body", 'tags')
        widgets = {
            "body": SummernoteWidget(),
            'tags': forms.CheckboxSelectMultiple(choices=TAG_CHOICES)
            # 'bar': SummernoteInplaceWidget(),
        }

    def clean_tags(self):
        '''
        The tags are not rendering well, therefore
        1. use regex to extract only words and not the symbols from the tag list
        2. convert the word into a list
        3. for each element in the list, strip out the spaces
        '''
        data = (self.cleaned_data['tags'])
        valid = re.sub(r'[^\w]', ' ', str(data))
        vd = valid.split(' ')
        delete_empty = [ele for ele in vd if ele.strip()]
        return delete_empty
