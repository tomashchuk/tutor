from django.urls import path, include
from rest_framework import routers

from .views import (
    CourseViewSet,
    CourseCategoryViewSet,
    TopicViewSet,
    MaterialViewSet,
    QuestionViewSet,
    UserCourseViewSet,
    StudentMaterialViewSet,
    AnswerOptionViewSet,
    AnswerViewSet,
)

router = routers.DefaultRouter()
router.register(r"course", CourseViewSet)
router.register(r"material", MaterialViewSet)
router.register(r"question", QuestionViewSet)
router.register(r"topic", TopicViewSet)
router.register(r"student-material", StudentMaterialViewSet)
router.register(r"answer-option", AnswerOptionViewSet)
router.register(r"answer", AnswerViewSet)
router.register(r"user-course", UserCourseViewSet)

urlpatterns = [
    path(
        "course-category/",
        CourseCategoryViewSet.as_view({"get": "list"}),
        name="course_category",
    ),
    path("", include(router.urls)),
]
