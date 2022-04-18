from django.urls import path

from .views import (
    CourseViewSet, CourseCategoryViewSet, TopicViewSet
)

urlpatterns = [
    path("course/", CourseViewSet.as_view({"get": "list"}), name="course"),
    path("course-category/", CourseCategoryViewSet.as_view({"get": "list"}), name="course_category"),
    path("topic/", TopicViewSet.as_view({"get": "list"}), name="topic"),

]