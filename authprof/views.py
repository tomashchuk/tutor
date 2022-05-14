from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import AuthUser
from .serializers import (
    UserSerializer,
    TokenObtainPairSerializer,
    PasswordSerializer,
    UpdateUserSerializer,
    UpdatePasswordSerializer,
)


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    update_serializer_class = UpdateUserSerializer
    queryset = AuthUser.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        `Update User`
        """
        partial = kwargs.pop("partial", False)
        user = self.request.user
        serializer = self.update_serializer_class(
            user, data=request.data, partial=partial
        )
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        user.set_password(serializer.validated_data["password"])
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=True, methods=["put"])
    def change_password(self, request, pk=None):
        # user = self.get_object()
        user = self.request.user
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid() and check_password(
            serializer.validated_data["old_password"], user.password
        ):
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"status": "password set"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
