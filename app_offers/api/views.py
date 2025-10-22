from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from app_offers.models import Offer
from app_offers.api.permissions import IsBusinessUserOrReadOnly


from .serializers import OfferListSerializer, OfferCreateSerializer
from .filters import OfferFilter


class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['id']
    search_fields = ['title', 'description',]

    def get_permissions(self):
        return [IsAuthenticated(), IsBusinessUserOrReadOnly()] if self.request.method == 'POST' else [AllowAny()]

    def get_serializer_class(self):
        return OfferCreateSerializer if self.request.method == 'POST' else OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
