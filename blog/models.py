# models.py

from random import randint
from django.db import models
import uuid

def get_default_anonymous_username():
    return Comment.get_anonymous_username()

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Comment(models.Model):
    ANONYMOUS_USERNAME = {
        "first_name": ("Funny", "Cooked", "Baked", "Smelly", "Tiny", "Big", "Small", "Smart", "Scary", "Anonymous", "Handsome"),
        "last_name": ("Seagull", "Tiger", "Fish", "Cat", "Dog", "Mouse", "Rabbit", "Bird", "Lion", "Elephant", "Penguin", "Wolf")
    }

    @classmethod
    def get_anonymous_username(cls):
        first_name = cls.ANONYMOUS_USERNAME["first_name"][randint(0, len(cls.ANONYMOUS_USERNAME["first_name"])-1)]
        last_name = cls.ANONYMOUS_USERNAME["last_name"][randint(0, len(cls.ANONYMOUS_USERNAME["last_name"])-1)]
        return f"{first_name} {last_name}"

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100, default=get_default_anonymous_username)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"{self.username} - {self.post.title}"