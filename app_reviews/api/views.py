from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from app_offers.models import Offer

from .serializers import ReviewSerializer
from .filters import ReviewFilter


class ReviewListView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
