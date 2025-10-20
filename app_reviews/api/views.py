from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import generics, filters
from app_reviews.models import Review

from .serializers import ReviewSerializer
from .filters import ReviewFilter


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def perform_create(self, serializer):
        reviewer = self.request.user
        serializer.save(reviewer=reviewer)
