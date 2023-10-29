from rest_framework.permissions import BasePermission

from lessons.models import Subscription


class IsOwner(BasePermission):
    def has_permission(self, request, view):

        return request.user == view.get_object().owner


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='manager'):
            return True
        return False


class IsSubscriber(BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().user


class IsLessonSubscribed(BasePermission):
    def has_permission(self, request, view):

        subscription = Subscription.objects.filter(user=request.user, course=view.get_object().course)
        if subscription:
            return True
        return False


class IsCourseSubscribed(BasePermission):
    def has_permission(self, request, view):

        subscription = Subscription.objects.filter(user=request.user, course=view.get_object())
        if subscription:
            return True
        return False
