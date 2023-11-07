from rest_framework import serializers

from lessons.models import Course, Lesson, Subscription
from lessons.services import create_session
from lessons.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):

    lesson_counter = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    payment_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_payment_url(self, instance):
        return create_session(instance)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
