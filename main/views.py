import json

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render
from main.forms import ProjectForm
from main.models import Experience, Project


def show_main(request):
    experiences = Experience.objects.all().order_by('-started_at')

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
    }
    return render(request, "index.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Project created successfully!')
        return redirect('main:show_main')
    else:
        messages.error(request, 'Failed to create project. Please check the form.')
    context = {
        "form": form,
    }

    return render(request, 'projects_form.html', context)

def get_projects_json(request):
    projects = Project.objects.all()

    name_query = request.GET.get('name', '').strip()
    if name_query:
        projects = projects.filter(name__icontains=name_query)

    projects_json = serializers.serialize('json', projects)
    return HttpResponse(projects_json, content_type='application/json')
