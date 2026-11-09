from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Experience


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "name", "url", "description",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "star_count", "is_starred", "starred_by_names"]

    def validate_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Project name cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_url(self, value):
        if value and not value.lower().startswith(("http://", "https://")):
            raise serializers.ValidationError("Use an HTTP or HTTPS project URL.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(id=request.user.id).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(obj.starred_by.values_list("username", flat=True))


class ExperienceSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.BooleanField(read_only=True)

    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )

    class Meta:
        model = Experience
        fields = [
            'id',
            'title',
            'organization',
            'description',
            'category',
            'category_display',
            'thumbnail',
            'started_at',
            'ended_at',
            'is_ongoing',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        started_at = attrs.get('started_at', getattr(self.instance, 'started_at', None))
        ended_at = attrs.get('ended_at', getattr(self.instance, 'ended_at', None))

        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError({
                'ended_at': 'The end date cannot be earlier than the start date.'
            })

        return attrs