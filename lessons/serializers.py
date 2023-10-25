from rest_framework import serializers

from lessons.models import Course, Lesson
from lessons.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):

    lesson_counter = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'
