# forms.py
from django.forms import ModelForm, TextInput, Textarea
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from blog.models import Post, Comment

class PostForm(ModelForm):
    def clean_title(self):
        title = self.cleaned_data['title']
        if strip_tags(title) != title:
            raise ValidationError('Please enter plain text without HTML tags.')
        return title

    def clean_content(self):
        content = self.cleaned_data['content']
        if strip_tags(content) != content:
            raise ValidationError('Please enter plain text without HTML tags.')
        return content

    class Meta:
        model = Post
        fields = ['title', 'content']

        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
        }

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'maxlength': 255, "placeholder": "Enter title"}),
            'content': Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': "Enter content"}),
        }


class CommentForm(ModelForm):
    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        if strip_tags(username) != username:
            raise ValidationError('Please enter plain text without HTML tags.')
        return username

    def clean_content(self):
        content = self.cleaned_data['content']
        if strip_tags(content) != content:
            raise ValidationError('Please enter plain text without HTML tags.')
        return content

    class Meta:
        model = Comment
        fields = ['username', 'content']

        labels = {
            'username': 'Your Name',
            'content': 'Add a Comment',
        }

        widgets = {
            'username': TextInput(attrs={'class': 'retro-input', 'placeholder': 'Your name'}),
            'content': Textarea(attrs={'class': 'retro-textarea', 'rows': 1, 'placeholder': 'Add a comment'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
