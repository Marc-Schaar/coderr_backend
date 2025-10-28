from rest_framework import generics

from app_orders.models import Order
from .serializers import OrderSerializer


class OrdersListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
