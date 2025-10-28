from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsCustomerUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        if request.user.type.lower() == 'business':
            raise PermissionDenied("Mit einem Gechäftskonto dürfen keine Bestellungen erstellt werden.")
        return True
