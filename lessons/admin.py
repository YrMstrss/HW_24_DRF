from django.contrib import admin

from lessons.models import Lesson, Course, Subscription

admin.site.register(Lesson)

admin.site.register(Course)

admin.site.register(Subscription)
