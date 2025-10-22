from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsCustomerUserOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.type == 'business':
            raise PermissionDenied(
                "Mit einem Geschäftsprofil dürfen keine Bewertungen abgegeben werden."
            )

        return True


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.reviewer != request.user:
            raise PermissionDenied(
                "Du darfst nur deine eigenen Bewertungen bearbeiten oder löschen."
            )

        return True
