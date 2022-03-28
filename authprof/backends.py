from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework.exceptions import NotFound


class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        user_modal = get_user_model()
        try:
            email = kwargs.get("email")
            if not email:
                email = kwargs.get("username")
            user = user_modal.objects.get(email=email)
            if user.check_password(kwargs.get("password")):
                return user
        except user_modal.DoesNotExist:
            raise NotFound()
        return
