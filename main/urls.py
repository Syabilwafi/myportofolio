from django.urls import path
from main.views import (
    show_main,
    create_project,
    update_project,
    delete_project,
    get_projects_json,
    register,
    login_view,
    logout_view,
    toggle_star,
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-project/', create_project, name='create_project'),
    path('projects/<uuid:project_id>/update/', update_project, name='update_project'),
    path('projects/<uuid:project_id>/delete/', delete_project, name='delete_project'),
    path('api/projects/', get_projects_json, name='get_projects_json'),
    path('projects/<uuid:project_id>/star/', toggle_star, name='toggle_star'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]