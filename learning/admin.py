from django.contrib import admin
from .models import (
    CourseCategory,
    Course,
    Topic,
    Material,
    Quiz,
    AnswerOption,
    QuizQuestion,
    QuizAnswer,
    QuizResult,
)


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    pass


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    pass
