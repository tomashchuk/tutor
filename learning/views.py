from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from authprof.models import AuthUser
from .domain import swift_order_topics, swift_order_materials
from .models import (
    Course,
    CourseCategory,
    Topic,
    Material,
    Question,
    UserCourse,
    StudentMaterial,
    Answer,
    AnswerOption, Status,
)
from .serializers import (
    CourseSerializer,
    CourseCategorySerializer,
    TopicSerializer,
    MaterialSerializer,
    QuestionSerializer,
    UserCourseSerializer,
    StudentMaterialSerializer,
    AnswerSerializer,
    AnswerOptionSerializers,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "category_id",
                openapi.IN_QUERY,
                description="category id",
                type=openapi.TYPE_ARRAY,
                items=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "include_my",
                openapi.IN_QUERY,
                description=" ",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "include_my_tutor",
                openapi.IN_QUERY,
                description=" ",
                type=openapi.TYPE_INTEGER,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        category_id = self.request.query_params.getlist("category_id")
        include_my = self.request.query_params.get("include_my")
        include_my_tutor = self.request.query_params.get("include_my_tutor")
        queryset = self.queryset
        user = self.request.user
        if category_id:
            queryset = queryset.filter(category_id__in=category_id)
        if user.user_type == AuthUser.TUTOR:
            return queryset.filter(tutor=self.request.user)
        queryset = queryset.filter(public=True, active=True)
        if include_my == "true":
            courses_asigned_ids = UserCourse.objects.filter(user=self.request.user)
            courses_asigned_ids = [
                courses_asigned.course_id for courses_asigned in courses_asigned_ids
            ]
            queryset = queryset.filter(id__in=courses_asigned_ids)
        return queryset

    # def create(self, request, *args, **kwargs):
    #     self.serializer_class = CreateCourseSerializer
    #     return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        if not user or user.user_type != AuthUser.TUTOR:
            raise ValidationError()
        serializer.save(tutor=self.request.user)


class CourseCategoryViewSet(ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "course_id",
                openapi.IN_QUERY,
                description="course id",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        order = request.data.get("order", None)
        if order:
            instance = self.get_object()
            swift_order_topics(order, instance)
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        course_id = request.data["course"]
        last_topic = (
            self.queryset.filter(course_id=course_id).order_by("-order").first()
        )
        request.data["order"] = last_topic.order + 1 if last_topic else 1
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        if course_id:
            return self.queryset.filter(course_id=course_id)
        return self.queryset


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "topic_id",
                openapi.IN_QUERY,
                description="topic id",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        topic_id = request.data["topic"]
        last_material = (
            self.queryset.filter(topic_id=topic_id).order_by("-order").first()
        )
        request.data["order"] = last_material.order + 1 if last_material else 1
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        order = request.data.get("order", None)
        if order:
            instance = self.get_object()
            swift_order_materials(order, instance)
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        if topic_id:
            return self.queryset.filter(topic_id=topic_id)
        return self.queryset


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "quiz_id",
                openapi.IN_QUERY,
                description="quiz id",
                type=openapi.TYPE_INTEGER,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        material_id = request.data["material"]
        material = Material.objects.filter(id=material_id).first()
        if not material or not material.material_type == Material.TESTING:
            raise ValidationError()
        last_question = (
            self.queryset.filter(material_id=material_id).order_by("-order").first()
        )
        request.data["order"] = last_question.order + 1 if last_question else 1
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        order = request.data.get("order", None)
        if order:
            instance = self.get_object()
            swift_order_materials(order, instance)
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        quiz_id = self.request.query_params.get("material_id")
        if quiz_id:
            return self.queryset.filter(material_id=quiz_id)
        return self.queryset


class UserCourseViewSet(ModelViewSet):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer

    @action(detail=False, methods=["post"])
    def join_course_secret(self, request):
        secret_code = request.data.get("secret_code")
        if not secret_code or not request.user.is_student:
            raise ValidationError()
        course = Course.objects.filter(secret_code=secret_code).first()
        if not course:
            raise ValidationError("Course does not exist")
        if self.queryset.filter(user_id=request.user.id, course_id=course.id):
            raise ValidationError("You are already enrolled for this course")
        UserCourse.objects.create(user=request.user, course=course)
        return Response(status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]
        queryset = self.queryset.filter(user=self.request.user, course_id=course)
        if queryset:
            raise ValidationError("You are already enrolled for this course")
        serializer.save(user=self.request.user)


class StudentMaterialViewSet(ModelViewSet):
    queryset = StudentMaterial.objects.all()
    serializer_class = StudentMaterialSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user or user.user_type != AuthUser.STUDENT:
            raise ValidationError()
        serializer.save(student=self.request.user)


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user or user.user_type != AuthUser.STUDENT:
            raise ValidationError()
        data_list = []
        for data in request.data:
            data.update({"user": user.id})
            data_list.append(data)
        #     serializer = self.get_serializer(data=data)
        #     serializer.is_valid(raise_exception=True)
        #     self.perform_create(serializer)
        # return super(AnswerViewSet, self).list(self, request, *args, **kwargs)
        serializer = self.get_serializer(data=data_list, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        material = Question.objects.get(id=request.data[0].get("question")).material
        student_material = StudentMaterial.objects.get(material_id=material.id, student_id=user.id)
        student_material.status = Status.COMPLETED
        student_material.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer):
    #     user = self.request.user
    #     if not user or user.user_type != AuthUser.STUDENT:
    #         raise ValidationError()
    #     serializer.save(user=self.request.user)


class AnswerOptionViewSet(ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionSerializers
