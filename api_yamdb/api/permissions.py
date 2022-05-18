from rest_framework import permissions, status
from rest_framework.response import Response


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous is True:
            return False
        elif request.user.role != 'moderator':
            return False
        return True


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous is True:
            return False
        elif request.user.is_superuser is not True:
            return False
        return True


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous is True:
            return False
        elif request.user.role != 'admin':
            return False
        return True


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous is True:
            return False
        elif request.user.role != 'user':
            return False
        return True
