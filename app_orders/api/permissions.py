from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsCustomerUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        if request.user.type.lower() == 'business':
            raise PermissionDenied("Mit einem Gechäftskonto dürfen keine Bestellungen erstellt werden.")
        return True


class IsBusinessUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        if request.user.is_staff:
            return True

        if request.user != obj.business_user:
            raise PermissionDenied(
                "Nur das Geschäftskonto, das die Bestellung erhalten hat, kann diese Aktion durchführen.")
        return True


class IsAdminUserToDeleteOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" and not request.user.is_staff:
            raise PermissionDenied("Nur Administratoren können Bestellungen löschen.")
        return True
