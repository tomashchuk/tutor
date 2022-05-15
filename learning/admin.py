from django.contrib import admin
from .models import (
    CourseCategory,
    Course,
    Topic,
    Material,
    AnswerOption,
    Question,
    Answer,
    StudentMaterial,
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


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentMaterial)
class StudentMaterialAdmin(admin.ModelAdmin):
    pass
