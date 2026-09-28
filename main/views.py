import json
from datetime import datetime
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from main.forms import ProjectForm, CustomUserCreationForm, CustomAuthenticationForm
from main.models import Experience, Project


# Helper function to check if user is superuser or editor
def is_superuser_or_editor(user):
    return user.is_superuser or user.groups.filter(name='Editor').exists()


# Decorator to check superuser or editor permission
def superuser_or_editor_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:login')
        if not is_superuser_or_editor(request.user):
            return HttpResponseForbidden("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)
    return wrapped_view


# Decorator to check superuser only
def superuser_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:login')
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)
    return wrapped_view



def show_main(request):
    experiences = Experience.objects.all().order_by('-started_at')
    projects = Project.objects.all()
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukannya')

    # Determine user permissions
    is_superuser = request.user.is_superuser
    is_editor = is_superuser_or_editor(request.user)
    can_edit = is_editor
    can_delete = is_superuser
    can_create = is_superuser
    can_star = request.user.is_authenticated

    context = {
        "name": "Syabil Wafi",
        "npm": "2506657371",
        "class": "PBP-B",
        "bio": (
            "Computer Science undergraduate at the University of Indonesia with experience in data science, operations, and leadership. I've worked on web-based projects, "
            "focusing on front-end development and UI/UX, while also contributing to startup operations and actively participating in organizations. I'm continuously "
            "developing my skills in programming and problem-solving, and I'm eager to contribute to impactful projects, grow as a technologist, and collaborate with others to create meaningful solutions."
        ),
        "experiences": experiences,
        "projects": projects,
        "last_login": last_login,
        "is_superuser": is_superuser,
        "is_editor": is_editor,
        "can_edit": can_edit,
        "can_delete": can_delete,
        "can_create": can_create,
        "can_star": can_star,
    }
    return render(request, "index.html", context)

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

def get_projects_json(request):
    projects = Project.objects.all()

    name_query = request.GET.get('name', '').strip()
    if name_query:
        projects = projects.filter(name__icontains=name_query)

    projects_list = []
    for project in projects:
        projects_list.append({
            'pk': str(project.id),
            'model': 'main.project',
            'fields': {
                'name': project.name,
                'url': project.url,
                'description': project.description,
                'stars_count': project.starred_by.count(),
                'is_starred': project.starred_by.filter(pk=request.user.id).exists() if request.user.is_authenticated else False,
            }
        })

    return HttpResponse(json.dumps(projects_list), content_type='application/json')

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
            max_age=60*60*24*7  # 7 days
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

    return JsonResponse({
        'success': True,
        'is_starred': is_starred,
        'stars_count': project.starred_by.count()
    })
