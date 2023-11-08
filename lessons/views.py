from rest_framework import viewsets, generics

from lessons.models import Course, Lesson, Subscription
from lessons.paginators import LessonPaginator
from lessons.permissions import IsManager, IsOwner, IsSubscriber, IsLessonSubscribed, IsCourseSubscribed
from lessons.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lessons.tasks import send_message


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LessonPaginator

    def get(self, request, **kwargs):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_permissions(self):
        if self.action == 'update' or self.action == 'partial_update' or self.action == 'retrieve':
            permission_classes = [IsManager | IsOwner | IsCourseSubscribed]
        elif self.action == 'delete':
            permission_classes = [~IsManager | IsOwner]
        elif self.action == 'create':
            permission_classes = [~IsManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        send_message.delay(course.pk, 'course', 'update')


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsManager]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

        send_message.delay(lesson.pk, 'lesson', 'create')


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get(self, request, **kwargs):
        queryset = Lesson.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

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
    permission_classes = [IsOwner | IsManager | IsLessonSubscribed]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager | IsOwner]

    def perform_update(self, serializer):
        lesson = serializer.save()
        send_message.delay(lesson.pk, 'lesson', 'update')


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
