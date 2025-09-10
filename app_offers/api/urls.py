from django.urls import include, path
from .views import OfferView

urlpatterns = [
    path("offers/", OfferView.as_view(), name="offer-list")
]