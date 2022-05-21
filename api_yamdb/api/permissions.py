from rest_framework import permissions


class IsAnonimous(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_anonymous is True
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_anonymous is False and
                request.user.role == 'moderator'
        )


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_anonymous is False and
                request.user.is_superuser is True
        )


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_anonymous is False and
                request.user.role == 'admin'
        )


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_anonymous is False and
                request.user.role == 'user'
        )
