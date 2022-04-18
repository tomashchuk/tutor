from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import (
    Course, CourseCategory, Topic
)
from .serializers import (
    CourseSerializer, CourseCategorySerializer, TopicSerializer
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseCategoryViewSet(ModelViewSet):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('category_id', openapi.IN_QUERY, description="category id", type=openapi.TYPE_INTEGER)]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id")
        if category_id:
            return self.queryset.filter(course_id=category_id)
        raise ValidationError()
