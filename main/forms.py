from django.forms import ModelForm, TextInput, Textarea, URLInput, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm as BaseAuthenticationForm

from main.models import Project
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from urllib.parse import urlsplit

class ProjectForm(ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if strip_tags(name) != name:
            raise ValidationError('Please enter plain text without HTML tags.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if strip_tags(description) != description:
            raise ValidationError('Please enter plain text without HTML tags.')
        return description

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and strip_tags(url) != url:
            raise ValidationError('Please enter a valid project URL.')
        if url and urlsplit(url).scheme.lower() not in ('http', 'https'):
            raise ValidationError('Use an HTTP or HTTPS project URL.')
        return url

    class Meta:
        model = Project
        fields = ['name', 'url', 'description']

        labels = {
            'name': 'Project Name',
            'url': 'Project URL',
            'description': 'Project Description',
        }

        widgets = {
            'name': TextInput(attrs={'class': 'retro-input', 'maxlength': 255, 'placeholder': 'Enter project name'}),
            'url': URLInput(attrs={'class': 'retro-input', 'maxlength': 255, 'placeholder': 'Enter project URL'}),
            'description': Textarea(attrs={'class': 'retro-textarea', 'rows': 5, 'placeholder': 'Enter project description'}),
        }


class CustomUserCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'retro-input',
            'placeholder': 'Enter username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'retro-input',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'retro-input',
            'placeholder': 'Confirm password'
        })


class CustomAuthenticationForm(BaseAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'retro-input',
            'placeholder': 'Enter username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'retro-input',
            'placeholder': 'Enter password'
        })
