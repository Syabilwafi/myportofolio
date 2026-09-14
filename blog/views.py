# views.py
from django.shortcuts import render
from .models import Post


def show_blog(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'name': 'Syabil Wafi',
    }
    return render(request, 'blog.html', context)
