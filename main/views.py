from django.shortcuts import render
from main.models import Experience


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