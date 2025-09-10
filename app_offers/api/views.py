from django.urls import include, path
from rest_framework import generics
from rest_framework.permissions import AllowAny

from app_offers.models import Offer
from .serializers import OfferSerializer

class OfferView(generics.ListAPIView):
    queryset= Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [AllowAny]

