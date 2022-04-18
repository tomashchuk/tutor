from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.core.validators import MinLengthValidator

from authprof.models import AuthUser
from shared.models import BaseModel


class CourseCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Course(BaseModel):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    public = models.BooleanField(default=False)

    tutor = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name="courses")
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    secret_code = models.CharField(max_length=255, validators=[MinLengthValidator(6)])

    def __str__(self):
        return self.name


class Topic(BaseModel):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="topics")

    def __str__(self):
        return self.name

# class MaterialMedia(BaseModel):
#     IMAGE
#     type =


class Material(BaseModel):
    HOMEWORK = "homework"
    LESSON = "lesson"
    TESTING = "testing"
    TYPE = (
        (HOMEWORK, "Homework"),
        (LESSON, "Lesson"),
        (TESTING, "Testing"),
    )
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Quiz(BaseModel):
    time_to_complete = models.PositiveSmallIntegerField(null=True)

    material = models.ForeignKey(Material, on_delete=models.CASCADE)


class AnswerOption(BaseModel):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class QuizQuestion(BaseModel):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200)
    possible_answers = models.ManyToManyField(AnswerOption)
    correct = models.ForeignKey(AnswerOption, related_name="correct", default=None, on_delete=models.CASCADE)


class QuizAnswer(BaseModel):
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.PROTECT)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)


class QuizResult(BaseModel):
    FAILED = "failed"
    PASSED = "passed"
    IN_PROGRESS = "in_progress"

    STATUS = (
        (IN_PROGRESS, "In Progress"),
        (PASSED, "Passed"),
        (FAILED, "Failed"),
    )

    status = models.CharField(max_length=20, choices=STATUS, default=IN_PROGRESS)
    quiz = models.ForeignKey(Quiz, on_delete=models.PROTECT)
    student = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
