# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from django.utils.timesince import timesince
from .forms import CommentForm, PostForm
from .models import Comment, Post
from main.constants import PROFILE


def show_blog(request):
    # Determine user permissions
    can_create = request.user.is_superuser
    can_delete = request.user.is_superuser

    context = {
        'comment_form': CommentForm(),
        'name': PROFILE['name'],
        'can_create': can_create,
        'can_delete': can_delete,
    }
    return render(request, 'blog.html', context)


@require_GET
def get_posts_json(request):
    posts = Post.objects.prefetch_related('comment_set').all().order_by('-created_at')
    query = request.GET.get('q', '').strip()
    if query:
        posts = posts.filter(title__icontains=query) | posts.filter(content__icontains=query)
    payload = [{
        'id': str(post.pk),
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.strftime('%b %d, %Y'),
        'comments': [{
            'username': comment.username,
            'content': comment.content,
            'time': f'{timesince(comment.created_at)} ago',
        } for comment in post.comment_set.all()],
    } for post in posts]
    response = JsonResponse(payload, safe=False)
    response['Cache-Control'] = 'private, no-store'
    return response


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
    if not post_id:
        messages.error(request, 'Choose a post before submitting a comment.')
        return redirect('blog:show_blog')

    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        if not comment.username or not comment.username.strip():
            comment.username = Comment.get_anonymous_username()
        comment.save()
        messages.success(request, 'Comment posted successfully!')
    else:
        messages.error(request, 'Comment could not be posted. Check the name and comment text.')
    return redirect('blog:show_blog')


@require_POST
def create_post_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please log in first.'}, status=401)
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Only superusers can create posts.'}, status=403)

    form = PostForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            'success': False,
            'message': 'Please correct the form.',
            'errors': form.errors.get_json_data(),
        }, status=400)

    post = form.save()
    return JsonResponse({
        'success': True,
        'message': 'Post created successfully!',
        'post': {
            'id': str(post.pk),
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at.strftime('%b %d, %Y'),
        },
    }, status=201)
