"""Permission helpers shared across portfolio apps."""

from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Allow public reads, owner writes, and Editor updates."""

    message = "Only the portfolio owner or an Editor can update projects."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )


def is_superuser_or_editor(user):
    """Return whether a user can edit portfolio content."""
    return user.is_superuser or user.groups.filter(name="Editor").exists()


def superuser_or_editor_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:login")
        if not is_superuser_or_editor(request.user):
            return HttpResponseForbidden("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)

    return wrapped_view


def superuser_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("main:login")
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)

    return wrapped_view
