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

class CommentRewiewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user.is_staff
                or request.user.is_superuser
            )
        return False