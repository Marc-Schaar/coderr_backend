from django.urls import include, path
from .views import ReviewListView, ReviewDetailView

urlpatterns = [
    path("reviews/", ReviewListView.as_view(), name="reviews-list"),
    path("reviews//<int:pk>", ReviewDetailView.as_view(), name="reviews-detail"),
]
