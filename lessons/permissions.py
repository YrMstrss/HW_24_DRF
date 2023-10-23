from rest_framework.permissions import BasePermission


class IsManagerOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='manager'):
            return True

        return request.user == view.get_object().owner


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
