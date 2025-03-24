from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка на владельца"""

    def has_object_permission(self, request, view, obj):

        if obj.user == request.user:
            return True
        return False


class IsUser(permissions.BasePermission):
    """Проверка возможность редактировать только своих данных"""

    def has_object_permission(self, request, view, obj):

        if obj == request.user:
            return True
        return False
