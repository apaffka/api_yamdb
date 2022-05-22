from rest_framework import permissions


class IsAnonimous(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous is True


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_anonymous is False and
            request.user.role == 'moderator')


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_anonymous is False and
            request.user.is_superuser is True)


class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_anonymous is False and
            request.user.role == 'admin')


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_anonymous is False and
            request.user.role == 'user')


# CommentRewiewPermission
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
