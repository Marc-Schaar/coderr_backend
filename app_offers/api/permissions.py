from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsBusinessUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.type.lower() == 'customer':
            raise PermissionDenied("Mit einem Kundenprofil dürfen keine Angebote erstellt werden.")
        return True
