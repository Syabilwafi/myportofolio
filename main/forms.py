from django.forms import ModelForm, TextInput, Textarea, URLInput

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
            'name': TextInput(attrs={'class': 'form-control', 'maxlength':255, "placeholder": "Enter project name"}),
            'url': URLInput(attrs={'class': 'form-control', 'maxlength':255, "placeholder": "Enter project URL"}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "Enter project description"}),
        }