# forms.py
from django.forms import ModelForm, TextInput, Textarea
from blog.models import Post, Comment

class PostForm(ModelForm):
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