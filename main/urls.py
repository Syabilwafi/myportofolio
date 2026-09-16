from django.urls import path
from main.views import show_main, create_project, get_projects_json

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-project/', create_project, name='create_project'),
    path("api/projects/", get_projects_json, name="get_projects_json")
]