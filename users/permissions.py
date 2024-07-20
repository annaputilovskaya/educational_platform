from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Проверка прав доступа владельца объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUser(BasePermission):
    """
    Проверка прав доступа пользователя к собсвенному профилю.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
