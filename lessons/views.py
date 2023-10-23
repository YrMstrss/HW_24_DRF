from rest_framework import viewsets, generics

from lessons.models import Course, Lesson
from lessons.permissions import IsManagerOrOwner, IsSuperuser
from lessons.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsManagerOrOwner]
        elif self.action == 'delete' or self.action == 'create':
            permission_classes = [IsSuperuser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsSuperuser]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager'):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManagerOrOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManagerOrOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsSuperuser]
