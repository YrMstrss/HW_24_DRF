from rest_framework.permissions import BasePermission

from lessons.models import Subscription


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()


class IsSubscriber(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class IsLessonSubscribed(BasePermission):
    def has_permission(self, request, view):
        return Subscription.objects.filter(user=request.user).exists()


class IsCourseSubscribed(BasePermission):
    def has_permission(self, request, view):
        return Subscription.objects.filter(user=request.user,).exists()