from rest_framework import viewsets, generics

from lessons.models import Course, Lesson, Subscription
from lessons.permissions import IsManager, IsOwner, IsSubscriber, IsLessonSubscribed, IsCourseSubscribed
from lessons.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'retrieve':
            permission_classes = [IsManager, IsOwner, IsCourseSubscribed]
        elif self.action == 'delete':
            permission_classes = [~IsManager, IsOwner]
        elif self.action == 'create':
            permission_classes = [~IsManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsManager]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='manager'):
            return Lesson.objects.all()

        queryset = Lesson.objects.filter(owner=user)

        subscriptions = Subscription.objects.filter(user=user)
        if subscriptions:
            for subscription in subscriptions:
                course = subscription.course
                lesson_set = Lesson.objects.filter(course=course)
                queryset = set(queryset | lesson_set)

        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsManager, IsLessonSubscribed]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        subscription = serializer.save()
        subscription.user = self.request.user
        subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [IsSubscriber]
