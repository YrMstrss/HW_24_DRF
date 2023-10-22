from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView

from lessons.models import Course
from lessons.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
