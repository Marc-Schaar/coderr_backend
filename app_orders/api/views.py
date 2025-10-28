from rest_framework import generics

from app_orders.models import Order
from .serializers import OrderSerializer


class OrdersListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.type == "business":
            return Order.objects.filter(business_user=user)
        elif user.type == "customer":
            return Order.objects.filter(customer_user=user)

        return Order.objects.none()
