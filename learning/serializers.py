from rest_framework import serializers
from .models import (
    Course, CourseCategory, Topic, Material, Quiz, QuizQuestion, AnswerOption, UserCourse
)


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
        )


class CourseSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)
    user_status = serializers.SerializerMethodField()

    def get_user_status(self, obj):
        request = self.context.get("request", None)
        if not request.user:
            return None
        try:
            user_course = UserCourse.objects.get(course_id=obj.id, user_id=request.user.id)
            return user_course.status
        except UserCourse.DoesNotExist:
            return None


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


class AnswerOptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = "__all__"


class QuizQuestionSerializer(serializers.ModelSerializer):
    possible_answers = AnswerOptionSerializers(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ["text", "order", "possible_answers"]


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = "__all__"
