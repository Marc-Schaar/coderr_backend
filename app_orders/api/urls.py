from django.urls import path
from .views import OrdersListView, OrderDetailView

urlpatterns = [
    path("orders/", OrdersListView.as_view(), name="order-list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order-detail"),

]
