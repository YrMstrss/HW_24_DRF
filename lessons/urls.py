from django.urls import path

from lessons.apps import LessonsConfig
from rest_framework.routers import DefaultRouter

from lessons.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = LessonsConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create', LessonCreateAPIView.as_view(), name='create-lesson'),
    path('lesson/', LessonListAPIView.as_view(), name='list-lesson'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='view-lesson'),
    path('lesson/edit/<int:pk>', LessonUpdateAPIView.as_view(), name='edit-lesson'),
    path('lesson/delete/<int:pk>', LessonDestroyAPIView.as_view(), name='delete-lesson'),
    path('subscribe/course/', SubscriptionCreateAPIView.as_view(), name='get-subscription'),
    path('subscribe/delete/<int:pk>', SubscriptionDestroyAPIView.as_view(), name='delete-subscription'),
] + router.urls
