from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import generics, filters
from app_reviews.models import Review

from .serializers import ReviewSerializer
from .filters import ReviewFilter
from .permissions import IsCustomerUserOrReadOnly


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [IsCustomerUserOrReadOnly]

    def perform_create(self, serializer):
        reviewer = self.request.user
        business_user = serializer.validated_data['business_user']

        if Review.objects.all().filter(business_user=business_user, reviewer=reviewer).exists():
            raise ValidationError("Du hast diesen Geschäftskunden bereits bewertet.")
        serializer.save(reviewer=reviewer)
