from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class AuthUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    STUDENT = "student"
    TUTOR = "tutor"
    TYPES = ((TUTOR, "Tutor"), (STUDENT, "Student"))

    username = models.CharField(
        _("username"),
        max_length=101,
        unique=False,
        help_text=_(
            "Required. 101 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        blank=True,
    )
    first_name = models.CharField(_("first name"), max_length=50, null=False)
    last_name = models.CharField(_("last name"), max_length=50, null=False)
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    user_type = models.CharField(choices=TYPES, max_length=10, default=STUDENT)

    def save(self, *args, **kwargs):
        self.username = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    # class Meta(AbstractUser.Meta):
    #     swappable = 'AUTH_USER_MODEL'
