from django.urls import path
from .views import OrdersListView, OrderDetailView, OrderCountView

urlpatterns = [
    path("orders/", OrdersListView.as_view(), name="order-list"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    path(
        "order-count/<int:pk>/",
        OrderCountView.as_view(completed=False),
        name="order-count",
    ),
    path(
        "completed-order-count/<int:pk>/",
        OrderCountView.as_view(completed=True),
        name="completed-order-count",
    ),
]
