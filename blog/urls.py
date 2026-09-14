from django.urls import path

from blog.views import show_blog
app_name = "blog"

urlpatterns = [
    path("", show_blog, name="show_blog"),
]