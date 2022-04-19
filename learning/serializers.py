from rest_framework import serializers
from .models import (
    Course, CourseCategory, Topic, Material, Quiz
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


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if hasattr(obj, "quiz"):
            return QuizSerializer(instance=obj.quiz, context=self.context).data

    class Meta:
        model = Material
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = "__all__"
