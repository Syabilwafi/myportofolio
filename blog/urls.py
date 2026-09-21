# blog/urls.py
from django.urls import path
from blog.views import show_blog, create_post, delete_post, create_comment

app_name = "blog"

urlpatterns = [
    path("", show_blog, name="show_blog"),
    path("create-post/", create_post, name="create_post"),
    path("delete-post/", delete_post, name="delete_post"),
    path("create-comment/", create_comment, name="create_comment"),
]