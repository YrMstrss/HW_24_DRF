from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserRetrieveAPIView, RegisterView

app_name = UsersConfig.name

urlpatterns = [
    path('edit/<int:pk>', UserUpdateAPIView.as_view(), name='edit-user'),
    path('<int:pk>', UserRetrieveAPIView.as_view(), name='view-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
]
