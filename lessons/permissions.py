from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):

        return request.user == view.get_object().owner


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='manager'):
            return True
        return False
