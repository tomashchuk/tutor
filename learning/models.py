from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.core.validators import MinLengthValidator

from authprof.models import AuthUser
from shared.models import BaseModel


class Status:
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    STATUS = (
        (TODO, "To Do"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
    )


class CourseCategory(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Course(BaseModel):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    public = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    tutor = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="courses"
    )
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    secret_code = models.CharField(
        max_length=255, validators=[MinLengthValidator(6)], unique=True
    )

    def __str__(self):
        return self.name


class UserCourse(BaseModel):
    user = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.STATUS, default=Status.TODO)


class Topic(BaseModel):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="topics")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


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
    order = models.PositiveSmallIntegerField(default=1)
    material_type = models.CharField(max_length=20, choices=TYPE, default=LESSON)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="materials")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class StudentMaterial(BaseModel):
    student = models.ForeignKey(AuthUser, on_delete=models.SET_NULL, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=Status.STATUS, default=Status.TODO)
    mark = models.PositiveIntegerField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    checked = models.BooleanField(default=False)

    due_date = models.DateTimeField(null=True, blank=True)


class AnswerOption(BaseModel):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Question(BaseModel):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField()
    possible_answers = models.ManyToManyField(AnswerOption)
    correct = models.ForeignKey(
        AnswerOption, related_name="correct", default=None, on_delete=models.CASCADE
    )

    coins = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.text


class Answer(BaseModel):
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.PROTECT)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    correct = models.BooleanField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.correct = self.answer_option == self.question.correct
        super().save(*args, **kwargs)
