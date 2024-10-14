from rest_framework import permissions
from api.constant import ADMIN, MODERATOR


class UserPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только пользователям."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == MODERATOR
                or request.user.role == ADMIN)


class ModeratorPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только модераторам."""

    def has_permission(self, request, view):
        return (
            (request.method in permissions.SAFE_METHODS
             or request.user.role == MODERATOR)
            or (request.method == 'DELETE'
                and request.user.role == MODERATOR)
        )


class AdminPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только админам."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.role == ADMIN or request.user.is_superuser
            )
        )


class AuthorPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только авторам."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and obj.author == request.user)
        )


class AdminOrReadOnlyPermissions(permissions.BasePermission):
    """
    Разрешение, позволяющее неавторизованным пользователям
    только безопасные методы, а администратору — любые действия.
    """

    def has_permission(self, request, view):
        return (
        request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and (request.user.role == ADMIN or request.user.is_superuser)))
