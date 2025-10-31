from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from app_orders.models import Order
from app_offers.models import OfferDetails
from .serializers import OrderSerializer
from .permissions import IsCustomerUserOrReadOnly, IsBusinessUserOrReadOnly, IsAdminUserToDeleteOnly


class OrdersListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomerUserOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.type == "business":
            return Order.objects.filter(business_user=user)
        elif user.type == "customer":
            return Order.objects.filter(customer_user=user)

        return Order.objects.none()

    def perform_create(self, serializer):
        offer_detail_id = self.request.data.get("offer_detail_id")

        if not offer_detail_id:
            raise NotFound("offer_detail_id ist erforderlich.")

        try:
            offer_detail = OfferDetails.objects.get(id=offer_detail_id)
        except OfferDetails.DoesNotExist:
            raise NotFound("OfferDetail wurde nicht gefunden.")

        serializer.save(
            customer_user=self.request.user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, IsAdminUserToDeleteOnly, IsBusinessUserOrReadOnly]
