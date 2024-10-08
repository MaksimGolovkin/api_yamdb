from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только пользователям."""

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or (
                request.user.role in ["user", "moderator", "admin"]
            )
        )


class ModeratorPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только модераторам."""

    def has_permission(self, request, view):
        return bool(
            (request.method in permissions.SAFE_METHODS
             or request.user.role == "user")
            or (request.method == 'DELETE'
                and request.user.role == "moderator")
        )


class AdminPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только админам."""

    def has_permission(self, request, view):
        return bool(request.user.role == "admin" or request.user.is_superuser)


class AuthorPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только авторам."""

    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user) or (
            request.user.role in ["moderator", "admin"]
        )
