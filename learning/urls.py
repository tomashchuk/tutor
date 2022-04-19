from django.urls import path

from .views import (
    CourseViewSet, CourseCategoryViewSet, TopicViewSet, MaterialViewSet
)

urlpatterns = [
    path("course/", CourseViewSet.as_view({"get": "list"}), name="course"),
    path("course-category/", CourseCategoryViewSet.as_view({"get": "list"}), name="course_category"),
    path("topic/", TopicViewSet.as_view({"get": "list"}), name="topic"),
    path("material/", MaterialViewSet.as_view({"get": "list"}), name="material"),

]