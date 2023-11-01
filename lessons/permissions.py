from rest_framework.permissions import BasePermission

from lessons.models import Subscription


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        return request.user == obj.owner


class IsManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='manager'):
            return True
        return False


class IsSubscriber(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsLessonSubscribed(BasePermission):
    def has_object_permission(self, request, view, obj):

        subscription = Subscription.objects.filter(user=request.user, course=obj.course)
        if subscription:
            return True
        return False


class IsCourseSubscribed(BasePermission):
    def has_object_permission(self, request, view, obj):

        subscription = Subscription.objects.filter(user=request.user, course=view.get_object())
        if subscription:
            return True
        return False
