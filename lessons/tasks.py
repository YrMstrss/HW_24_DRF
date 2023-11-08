from datetime import datetime, timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lessons.models import Lesson, Subscription, Course
from users.models import User


@shared_task
def send_message(pk, obj: str, method: str):
    if obj == 'lesson':
        instance = Lesson.objects.filter(pk=pk)
        course = instance.course
        subscription = Subscription.objects.filter(course=course)
        users = [user for user in subscription.users.email]
        if method == 'create':
            send_mail(
                subject=f'Изменения в курсе "{course.title}"',
                message=f'В курс "{course.title}" добавлен новый урок "{instance.title}"',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=users,
                fail_silently=False
            )
        elif method == 'update':
            send_mail(
                subject=f'Изменения в курсе "{course.title}"',
                message=f'В урок "{instance.title}" курса "{course.title}" были внесены изменения',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=users,
                fail_silently=False
            )
    else:
        instance = Course.objects.filter(pk=pk)
        subscription = Subscription.objects.filter(course=instance)
        users = [user for user in subscription.users.email]
        if method == 'update':
            send_mail(
                subject=f'Изменения в курсе "{instance.title}"',
                message=f'В курс "{instance.title}" были внесены изменения',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=users,
                fail_silently=False
            )


def check_user_activity():
    users = User.objects.filter(last_login__lt=datetime.now() - timedelta(days=30))
    for user in users:
        users.is_active = False
        user.save()
    users = User.objects.filter(last_login=None)
    for user in users:
        if user.date_joined < datetime.now() - timedelta(days=30):
            users.is_active = False
            user.save()
