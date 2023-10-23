from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager')


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
