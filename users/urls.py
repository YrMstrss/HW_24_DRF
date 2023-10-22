from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, UserRetrieveAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('user/edit/<int:pk>', UserUpdateAPIView.as_view(), name='edit-user'),
    path('user/<int:pk>', UserRetrieveAPIView.as_view(), name='view-user'),
]
