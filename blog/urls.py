# blog/urls.py
from django.urls import path
from blog.views import show_blog, create_post, delete_post

app_name = "blog"

urlpatterns = [
    path("", show_blog, name="show_blog"),
    path("create-post/", create_post, name="create_post"),
    path("delete-post/", delete_post, name="delete_post"),
]