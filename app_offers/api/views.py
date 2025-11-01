from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from app_offers.models import Offer, OfferDetails
from app_offers.api.permissions import IsBusinessUserOrReadOnly, IsOwnerOrReadOnly


from .serializers import OfferListSerializer, OfferCreateSerializer, OfferUpdateSerializer, OfferDetailSerializer, OfferDetailsSerializer
from .filters import OfferFilter


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for offers.
    Sets default page size and allows client to set page size up to a maximum.
    """
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferView(generics.ListCreateAPIView):
    """
    API view for listing all offers and creating new offers.
    Supports filtering, searching, ordering, and pagination. Only authenticated business users can create offers.
    """
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


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a specific offer.
    Only the owner can update or delete the offer. Uses the offer's primary key for lookup.
    """
    queryset = Offer.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        return OfferUpdateSerializer if self.request.method == 'PATCH' else OfferDetailSerializer


class OfferDetailDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving the details of a specific offer detail object by primary key.
    """
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailsSerializer
    lookup_field = 'pk'
