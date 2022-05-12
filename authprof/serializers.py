from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as JwtTokenObtainPairSerializer,
)

from authprof.models import AuthUser


class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().EMAIL_FIELD


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
            "password",
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UpdateUserSerializer(UserSerializer):
    class Meta:
        model = AuthUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30, min_length=8)


class UpdatePasswordSerializer(PasswordSerializer):
    old_password = serializers.CharField(max_length=30, min_length=8)
