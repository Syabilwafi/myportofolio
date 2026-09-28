# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm


def is_superuser_or_editor(user):
    """Check if user is superuser or in Editor group"""
    return user.is_superuser or user.groups.filter(name='Editor').exists()


def show_blog(request):
    posts = Post.objects.prefetch_related('comment_set').all().order_by('-created_at')

    # Determine user permissions
    can_create = request.user.is_superuser
    can_edit = is_superuser_or_editor(request.user)
    can_delete = request.user.is_superuser
    can_comment = True  # Anyone can comment

    context = {
        'posts': posts,
        'comment_form': CommentForm(),
        'name': 'Syabil Wafi',
        'can_create': can_create,
        'can_edit': can_edit,
        'can_delete': can_delete,
        'can_comment': can_comment,
    }
    return render(request, 'blog.html', context)


@login_required(login_url='/login/')
def create_post(request):
    # Only superusers can create posts
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to create posts.')
        return redirect('blog:show_blog')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog:show_blog')
        else:
            messages.error(request, 'Failed to create post. Please check the form.')

    return redirect('blog:show_blog')


@login_required(login_url='/login/')
@require_POST
def delete_post(request):
    # Only superusers can delete posts
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to delete posts.")

    post_id = request.POST.get('post_id')
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        post.delete()
        messages.success(request, 'Post deleted successfully!')
    return redirect('blog:show_blog')


@require_POST
def create_comment(request):
    post_id = request.POST.get('post_id')
    if post_id:
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if not comment.username or not comment.username.strip():
                comment.username = Comment.get_anonymous_username()
            comment.save()
            messages.success(request, 'Comment posted successfully!')
    return redirect('blog:show_blog')