from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """
    Проверка прав доступа модератора.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderator").exists()


class IsOwner(BasePermission):
    """
    Проверка прав доступа владельца курса/урока.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
