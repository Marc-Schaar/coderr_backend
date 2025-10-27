from django.urls import include, path
from .views import OfferView, OfferDetailView, OfferDetailDetailView

urlpatterns = [
    path("offers/", OfferView.as_view(), name="offer-list"),
    path("offers/<int:pk>", OfferDetailView.as_view(), name="offer-detail"),
    path("offerdetails/<int:pk>", OfferDetailDetailView.as_view(), name="offer-details")
]
