from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsCustomerUserOrReadOnly(BasePermission):
    """
    Permission class that allows only customer users to create orders.
    Business users are restricted to read-only access for orders.
    """
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        if request.user.type.lower() == 'business':
            raise PermissionDenied("Mit einem Gechäftskonto dürfen keine Bestellungen erstellt werden.")
        return True


class IsBusinessUserOrReadOnly(BasePermission):
    """
    Permission class that allows only the business user who received the order to modify it.
    Read-only access is allowed for all users and staff can always modify.
    """
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
    """
    Permission class that allows only admin users to delete orders.
    All users can perform other actions if permitted by other rules.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" and not request.user.is_staff:
            raise PermissionDenied("Nur Administratoren können Bestellungen löschen.")
        return True
