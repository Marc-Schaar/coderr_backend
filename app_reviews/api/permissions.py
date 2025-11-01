from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsCustomerUserOrReadOnly(BasePermission):
    """
    Permission class that allows only customer users to create reviews.
    Business users are restricted from submitting reviews.
    """

    def has_permission(self, request, view):
        if request.user.type.lower() == "business":
            raise PermissionDenied(
                "Mit einem Geschäftsprofil dürfen keine Bewertungen abgegeben werden."
            )

        return True


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission class that allows only the review owner to edit or delete the review.
    Other users are denied modification access.
    """

    def has_object_permission(self, request, view, obj):
        if obj.reviewer != request.user:
            raise PermissionDenied(
                "Du darfst nur deine eigenen Bewertungen bearbeiten oder löschen."
            )

        return True
