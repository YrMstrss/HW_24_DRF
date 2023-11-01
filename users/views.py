from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsCurrentUser
from users.serializers import UserSerializer, UserSerializerForOthers


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if int(self.request.user.pk) == int(self.kwargs["pk"]):
            return UserSerializer
        else:
            return UserSerializerForOthers


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsCurrentUser]


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
