from rest_framework import serializers
from .models import (
    Course, CourseCategory, Topic
)


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
        )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = "__all__"
