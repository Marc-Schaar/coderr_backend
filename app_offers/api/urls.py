from django.urls import include, path
from .views import OfferView, OfferDetailView

urlpatterns = [
    path("offers/", OfferView.as_view(), name="offer-list"),
    path("offers/<int:pk>", OfferDetailView.as_view(), name="offer-detail")
]
