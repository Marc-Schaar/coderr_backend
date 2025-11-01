from rest_framework import generics
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from app_orders.models import Order
from app_offers.models import OfferDetails
from .serializers import OrderSerializer
from .permissions import (
    IsCustomerUserOrReadOnly,
    IsBusinessUserOrReadOnly,
    IsAdminUserToDeleteOnly,
)


class OrdersListView(generics.ListCreateAPIView):
    """
    API view for listing all orders for the authenticated user and creating new orders.
    Business users see their received orders, customers see their placed orders. Only customers can create orders.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsCustomerUserOrReadOnly]

    def get_queryset(self):
        """
        Returns the queryset of orders for the current user, filtered by user type.
        """
        user = self.request.user
        if user.type == "business":
            return Order.objects.filter(business_user=user)
        elif user.type == "customer":
            return Order.objects.filter(customer_user=user)

        return Order.objects.none()

    def perform_create(self, serializer):
        """
        Creates a new order based on the provided offer_detail_id and request user.
        Raises NotFound if the offer detail does not exist or is missing.
        """
        offer_detail_id = self.request.data.get("offer_detail_id")

        try:
            offer_detail_id = int(offer_detail_id)
        except (TypeError, ValueError):
            raise ValidationError(
                "offer_detail_id ist muss eine Zahl sein und darf nicht fehlen."
            )

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
    """
    API view for retrieving, updating, or deleting a specific order by primary key.
    Only admins can delete, business users can update, and all authenticated users can view.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "pk"
    permission_classes = [
        IsAuthenticated,
        IsAdminUserToDeleteOnly,
        IsBusinessUserOrReadOnly,
    ]


class OrderCountView(APIView):
    """
    API view for retrieving the count of orders for a business user.
    Returns either the count of completed or in-progress orders, depending on the view's state.
    """

    queryset = Order.objects.all()
    completed = False
    order_count = 0

    def get_order_count(self, business_user_id: int) -> int:
        """
        Returns the count of orders for a business user filtered by status (completed or in_progress).
        """
        status_filter = "completed" if self.completed else "in_progress"
        return Order.objects.filter(
            business_user_id=business_user_id, status=status_filter
        ).count()

    def get(self, request, pk=None):
        """
        Returns the order count for the given business user ID, or an error if no orders are found.
        """
        if not Order.objects.filter(business_user__id=pk).exists():
            return Response(
                {"error": "No orders found for the given business user ID."}, status=404
            )

        count = self.get_order_count(pk)
        key = "completed_order_count" if self.completed else "order_count"
        return Response({key: count})
