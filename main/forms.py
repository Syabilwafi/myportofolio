from django.forms import ModelForm, TextInput, Textarea, URLInput, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm as BaseAuthenticationForm

from main.models import Project

class ProjectForm(ModelForm):
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