from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from main.forms import ProjectForm, CustomUserCreationForm, CustomAuthenticationForm
from main.models import Experience, Project
from main.constants import ANONYMOUS_LOGIN_MESSAGE, PROFILE
from main.permissions import (
    is_superuser_or_editor,
    superuser_or_editor_required,
    superuser_required,
)

def show_main(request):
    last_login = request.COOKIES.get('last_login', ANONYMOUS_LOGIN_MESSAGE)

    is_superuser = request.user.is_superuser
    is_editor = is_superuser_or_editor(request.user)
    can_edit = is_editor
    can_delete = is_superuser
    can_create = is_superuser
    can_star = request.user.is_authenticated

    context = {
        **PROFILE,
        "last_login": last_login,
        "is_superuser": is_superuser,
        "is_editor": is_editor,
        "can_edit": can_edit,
        "can_delete": can_delete,
        "can_create": can_create,
        "can_star": can_star,
        "project_form": ProjectForm(),
    }
    return render(request, "index.html", context)


@require_http_methods(["GET"])
def get_experiences_json(request):
    experiences = Experience.objects.all().order_by('-started_at')
    payload = [{
        'id': str(experience.pk),
        'title': experience.title,
        'organization': experience.organization,
        'description': experience.description,
        'category': experience.get_category_display(),
        'started_at': experience.started_at.strftime('%b %Y'),
        'ended_at': experience.ended_at.strftime('%b %Y') if experience.ended_at else None,
    } for experience in experiences]
    response = JsonResponse(payload, safe=False)
    response['Cache-Control'] = 'private, no-store'
    return response

@superuser_required
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Project created successfully!')
        return redirect('main:show_main')
    else:
        if request.method == "POST":
            messages.error(request, 'Failed to create project. Please check the form.')

    context = {
        "form": form,
        "action": "Create",
    }
    return render(request, 'projects_form.html', context)


@superuser_or_editor_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Project updated successfully!')
        return redirect('main:show_main')
    else:
        if request.method == "POST":
            messages.error(request, 'Failed to update project. Please check the form.')

    context = {
        "form": form,
        "action": "Update",
        "project": project,
    }
    return render(request, 'projects_form.html', context)


@superuser_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('main:show_main')

    context = {
        "project": project,
    }
    return render(request, 'confirm_delete.html', context)

@require_http_methods(["GET"])
def get_projects_json(request):
    projects = Project.objects.annotate(stars_count=Count('starred_by'))
    starred_ids = set(request.user.starred_projects.values_list('pk', flat=True)) if request.user.is_authenticated else set()

    query = request.GET.get('q', request.GET.get('name', '')).strip()
    if query:
        projects = projects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    projects_list = []
    for project in projects:
        projects_list.append({
            'pk': str(project.id),
            'model': 'main.project',
            'fields': {
                'name': project.name,
                'url': project.url,
                'description': project.description,
                'star_count': project.stars_count,
                'stars_count': project.stars_count,
                'is_starred': project.pk in starred_ids,
            },
            'update_url': reverse('main:update_project', args=[project.pk]),
            'delete_url': reverse('main:delete_project', args=[project.pk]),
            'star_url': reverse('main:toggle_star', args=[project.pk]),
        })

    response = JsonResponse(projects_list, safe=False)
    response['Cache-Control'] = 'private, no-store'
    return response


@require_http_methods(["POST"])
def create_project_ajax(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Please log in first.'}, status=401)
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'message': 'Only superusers can create projects.'}, status=403)
    form = ProjectForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'success': False, 'message': 'Please correct the form.',
                             'errors': form.errors.get_json_data()}, status=400)
    project = form.save()
    return JsonResponse({'success': True, 'message': 'Project created successfully!',
                         'id': str(project.pk)}, status=201)

def register(request):
    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Syabil Wafi",
        "form": form,
    }
    return render(request, "register.html", context)

def login_view(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Selamat datang, {user.username}!")

        response = redirect("main:show_main")
        response.set_cookie(
            'last_login',
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            max_age=60*60*24*7
        )
        return response

    context = {
        "name": "Syabil Wafi",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Anda berhasil logout.")

    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

@login_required(login_url="/login/")
@require_http_methods(["POST"])
def toggle_star(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if project.starred_by.filter(id=request.user.id).exists():
        project.starred_by.remove(request.user)
        is_starred = False
    else:
        project.starred_by.add(request.user)
        is_starred = True

    star_count = project.starred_by.count()
    return JsonResponse({
        'success': True,
        'is_starred': is_starred,
        'star_count': star_count,
        'stars_count': star_count,
    })
