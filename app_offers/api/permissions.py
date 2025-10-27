from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsBusinessUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.type.lower() == 'customer':
            raise PermissionDenied("Mit einem Kundenprofil dürfen keine Angebote erstellt werden.")
        return True


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.user == request.user
