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
             or request.user.role == "moderator")
            or (request.method == 'DELETE'
                and request.user.role == "moderator")
        )


class AdminPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только админам."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return bool(request.user.role == "admin" or request.user.is_superuser)


class AuthorPermissions(permissions.BasePermission):
    """Кастомное разрешение на доступ к информации только авторам."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return obj.author == request.user
        return False


class IsAuthorModeratorAdminOrReadOnlyPermission(
    permissions.BasePermission
):
    """
    Кастомное разрешение на доступ к информации автору, модератору, админу.
    """
# в отличии от IsAuthenticatedOrReadOnly этот permissions еще проверяет роль
# Проверка роли нужна

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == "moderator"
                or request.user.role == "admin")
