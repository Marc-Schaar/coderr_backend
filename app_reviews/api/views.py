from django_filters.rest_framework import DjangoFilterBackend
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
        serializer.save(reviewer=self.request.user)

        # business_user = serializer.validated_data['business_user']
        # reviewer = self.request.user

        # if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
        #     raise ValidationError("Du hast diesen Business-User bereits bewertet!")

        # serializer.save(reviewer=reviewer)
