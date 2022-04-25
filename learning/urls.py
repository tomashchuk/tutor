from django.urls import path, include
from rest_framework import routers

from .views import (
    CourseViewSet,
    CourseCategoryViewSet,
    TopicViewSet,
    MaterialViewSet,
    QuizQuestionViewSet,
    UserCourseViewSet,
)

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'material', MaterialViewSet)

urlpatterns = [
    path("course-category/", CourseCategoryViewSet.as_view({"get": "list"}), name="course_category"),
    path("topic/", TopicViewSet.as_view({"get": "list"}), name="topic"),
    path("quiz-question/", QuizQuestionViewSet.as_view({"get": "list"}), name="quiz_question"),
    path("user-course/", UserCourseViewSet.as_view({"post": "create"}), name="user_course"),
    path("", include(router.urls)),
]
