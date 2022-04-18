from rest_framework import serializers
from .models import (
    Course, CourseCategory
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
