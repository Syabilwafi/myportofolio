# blog/urls.py
from django.urls import path
from blog.views import show_blog, get_posts_json, create_post, create_post_ajax, delete_post, create_comment

app_name = "blog"

urlpatterns = [
    path("", show_blog, name="show_blog"),
    path("api/posts/", get_posts_json, name="get_posts_json"),
    path("create-post/", create_post, name="create_post"),
    path("api/posts/create/", create_post_ajax, name="create_post_ajax"),
    path("delete-post/", delete_post, name="delete_post"),
    path("create-comment/", create_comment, name="create_comment"),
]
