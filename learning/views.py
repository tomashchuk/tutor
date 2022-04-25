from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import (
    Course, CourseCategory, Topic, Material, QuizQuestion, UserCourse
)
from .serializers import (
    CourseSerializer,
    CourseCategorySerializer,
    TopicSerializer,
    MaterialSerializer,
    QuizQuestionSerializer,
    UserCourseSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, description="category id", type=openapi.TYPE_ARRAY, items=openapi.TYPE_INTEGER),
            openapi.Parameter('include_my', openapi.IN_QUERY, description=" ", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        category_id = self.request.query_params.getlist("category_id")
        # include_my = int(self.request.query_params.get("include_my"))
        # courses_asigned_ids = []
        # if include_my:
        #     courses_asigned_ids = UserCourse.objects.filter(user=self.request.user)
        if category_id:
            return self.queryset.filter(category_id__in=category_id, public=True)
        return self.queryset.filter(public=True)


class CourseCategoryViewSet(ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('course_id', openapi.IN_QUERY, description="course id", type=openapi.TYPE_INTEGER)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        course_id = self.request.query_params.get("course_id")
        if course_id:
            return self.queryset.filter(course_id=course_id)
        raise ValidationError()


class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('topic_id', openapi.IN_QUERY, description="topic id", type=openapi.TYPE_INTEGER)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        if topic_id:
            return self.queryset.filter(topic_id=topic_id)
        raise ValidationError()


class QuizQuestionViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('quiz_id', openapi.IN_QUERY, description="quiz id", type=openapi.TYPE_INTEGER)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        quiz_id = self.request.query_params.get("quiz_id")
        if quiz_id:
            return self.queryset.filter(quiz_id=quiz_id)
        raise ValidationError()


class UserCourseViewSet(ModelViewSet):
    queryset = UserCourse.objects.all()
    serializer_class = UserCourseSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
