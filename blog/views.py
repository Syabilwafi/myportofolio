# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import PostForm

def show_blog(request):
    posts = Post.objects.all().order_by('-created_at')
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

@require_POST
def delete_post(request):
    post_id = request.POST.get('post_id')
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
    return redirect('blog:show_blog')