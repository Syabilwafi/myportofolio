import uuid
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)

    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        if self.organization:
            return f"{self.title} at {self.organization}"
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name