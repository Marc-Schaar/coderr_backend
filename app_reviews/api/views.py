from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from app_reviews.models import Review

from .serializers import ReviewSerializer, ReviewDetailSerializer
from .filters import ReviewFilter
from .permissions import IsCustomerUserOrReadOnly, IsOwnerOrReadOnly


class ReviewListView(generics.ListCreateAPIView):
    """
    API view for listing all reviews and creating a new review.
    Only authenticated customers can create reviews. Prevents duplicate reviews for the same business user.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ReviewFilter
    ordering_fields = ["updated_at", "rating"]
    permission_classes = [IsAuthenticated, IsCustomerUserOrReadOnly]

    def perform_create(self, serializer):
        """
        Handles creation of a new review, ensuring a customer cannot review the same business user twice.
        """
        reviewer = self.request.user
        business_user = serializer.validated_data["business_user"]

        if (
            Review.objects.all()
            .filter(business_user=business_user, reviewer=reviewer)
            .exists()
        ):
            raise ValidationError("Du hast diesen Geschäftskunden bereits bewertet.")
        serializer.save(reviewer=reviewer)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific review by primary key.
    Only the review owner can update or delete the review.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        """
        Updates the review and sets the updated_at timestamp to the current time.
        """
        instance = serializer.save()
        instance.updated_at = timezone.now()
        instance.save(update_fields=["updated_at"])
