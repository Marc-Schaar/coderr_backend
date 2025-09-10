from rest_framework import serializers
from app_accounts.models import User
from app_offers.models import Offer
from app_accounts.api.serializers import UserListSerializer


class OfferSerializer(serializers.ModelSerializer):
    user_details = UserListSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id', 
            'user',
            'title', 
            'image',
            'description',
            'created_at', 
            'updated_at', 
            'details', 
            'min_price', 
            'min_delivery_time',
            'user_details',
            ]

    