from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from app_accounts.models import User
from app_offers.models import Offer

from .serializers import OfferListSerializer, OfferCreateSerializer
from .filters import OfferFilter


class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100


class OfferView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    # serializer_class = OfferSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['id']
    search_fields = ['title', 'description',]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        creator_id = request.query_params.get('creator_id')

        if creator_id:
            if not User.objects.filter(id=creator_id).exists():
                return Response(
                    {"creator_id": "User does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().list(request, *args, **kwargs)
