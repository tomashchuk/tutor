from rest_framework import serializers
from authprof.models import AuthUser
from .models import (
    Course,
    CourseCategory,
    Topic,
    Material,
    Question,
    Answer,
    AnswerOption,
    UserCourse,
    StudentMaterial,
)
from rest_framework.fields import CurrentUserDefault


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = (
            "id",
            "name",
        )


class CourseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=CourseCategory.objects.all(), write_only=True
    )
    user_status = serializers.SerializerMethodField()

    def get_user_status(self, obj):
        request = self.context.get("request", None)
        if not request.user:
            return None
        try:
            user_course = UserCourse.objects.get(
                course_id=obj.id, user_id=request.user.id
            )
            return user_course.status
        except UserCourse.DoesNotExist:
            return None

    def to_representation(self, instance):
        data = super(CourseSerializer, self).to_representation(instance)
        data.update(
            {
                "category": CourseCategorySerializer(
                    instance=CourseCategory.objects.get(id=instance.category.id),
                    context=self.context,
                ).data
            }
        )
        return data

    class Meta:
        model = Course
        fields = "__all__"
        extra_kwargs = {"tutor": {"read_only": True}}


class CreateCourseSerializer(CourseSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=CourseCategory.objects.all(), write_only=True
    )

    def to_representation(self, instance):
        data = super(CourseSerializer, self).to_representation(instance)
        data.update(
            {
                "category": CourseCategorySerializer(
                    instance=CourseCategory.objects.get(id=instance.category.id),
                    context=self.context,
                ).data
            }
        )
        return data


class StudentMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMaterial
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super().__init__(many=many, *args, **kwargs)

    class Meta:
        model = Answer
        fields = "__all__"
        extra_kwargs = {"correct": {"read_only": True}, "earned_coins": {"read_only": True}}


class AnswerOptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ["id", "text", "coins", "correct"]
        # extra_kwargs = {"correct": {"write_only": True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # user = CurrentUserDefault()
        # if user.is_anonymous():
        #     return data
        # data.update(
        #     {
        #         "correct": instance.correct if user.is_tutor else None
        #     }
        # )
        return data


class QuestionSerializer(serializers.ModelSerializer):
    possible_answers = AnswerOptionSerializers(many=True)

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super().__init__(many=many, *args, **kwargs)

    class Meta:
        model = Question
        fields = ["id", "text", "order", "possible_answers", "multiple_answers", "material"]

    def create(self, validated_data):
        answers = validated_data.pop("possible_answers")
        question = Question.objects.create(**validated_data)
        request = self.context.get("request", None)
        for answer in answers:
            answer, created = AnswerOption.objects.get_or_create(
                text=answer["text"],
                question=question,
                defaults={"coins": answer["coins"], "correct": answer["correct"]}
            )
        return question

    def update(self, instance, validated_data):
        answers = validated_data.pop('possible_answers')
        for answer in answers:
            ingredient, created = AnswerOption.objects.update_or_create(
                text=answer["text"],
                question=instance.id,
                defaults={"coins": answer["coins"], "correct": answer["correct"]}
            )
        return super().update(instance, validated_data)


class MaterialSerializer(serializers.ModelSerializer):
    student_material = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True, read_only=True)

    def get_student_material(self, obj):
        request = self.context.get("request", None)
        if request.user == AuthUser.STUDENT:
            try:
                student_material = StudentMaterial.objects.get(
                    material_id=obj.id, student_id=request.user.id
                )
                return StudentMaterialSerializer(
                    instance=student_material, context=self.context
                ).data
            except StudentMaterial.DoesNotExist:
                return None

    class Meta:
        model = Material
        fields = "__all__"


class TopicSerializer(serializers.ModelSerializer):
    materials = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = "__all__"
        extra_kwargs = {"order": {"required": False}}


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}, "status": {"read_only": True}}
