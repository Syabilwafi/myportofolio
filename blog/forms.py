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
            'title': TextInput(attrs={'class': 'form-control', 'maxlength':255, "placeholder": "Enter title"}),
            'content': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "Enter content"}),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        labels = {
            'content': 'Comment',
        }

        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': "Enter comment"}),
        }
