from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm


def show_blog(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()

    context = {
        'posts': posts,
        'comments': comments,
        'name': 'Syabil Wafi',
    }
    return render(request, 'blog.html', context)


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:show_blog')
    return redirect('blog:show_blog')


def get_blog_post(request, post_id):
    posts = Post.objects.all()
    title_query = request.GET.get('title', '').strip()

    if title_query:
        posts = posts.filter(title__icontains=title_query)

    posts_json = serializers.serialize('json', posts)
    return HttpResponse(posts_json, content_type='application/json')