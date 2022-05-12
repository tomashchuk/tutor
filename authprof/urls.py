from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers

from .views import EmailTokenObtainPairView, UserView


router = routers.DefaultRouter()
router.register(r"profile", UserView)

urlpatterns = [
    path("register/", UserView.as_view({"post": "create"}), name="register"),
    path("profile/", UserView.as_view({"get": "retrieve", "patch": "partial_update"}), name="profile"),
    path("profile/change-password", UserView.as_view({"put": "change_password"}), name="profile_change_password"),
    path("token/obtain/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', include(router.urls))
]
