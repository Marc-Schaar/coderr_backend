from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsBusinessUserOrReadOnly(BasePermission):
    """
    Permission class that allows only business users to create or modify offers.
    Customers are restricted to read-only access and cannot create offers.
    """

    def has_permission(self, request, view):
        if request.user.type.lower() == "customer":
            raise PermissionDenied(
                "Mit einem Kundenprofil dürfen keine Angebote erstellt werden."
            )
        return True


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission class that allows object modification only by the owner.
    Read-only access is allowed for all users.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.user == request.user
