from rest_framework import serializers
from app_accounts.models import User
from app_offers.models import Offer, OfferDetails
from app_accounts.api.serializers import UserListSerializer


class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailsSerializer(many=True)
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


class OfferCreateSerializer(serializers.ModelSerializer):
   # user = serializers.PrimaryKeyRelatedField(read_only=True)
    details = OfferDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            # 'user',
            'title',
            'image',
            'description',
            'details',
        ]

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)

        created_details = []
        for detail_data in details_data:
            detail = OfferDetails.objects.create(offer=offer, **detail_data)
            created_details.append(detail)

        if details_data:
            offer.min_price = min(d['price'] for d in details_data)
            offer.min_delivery_time = min(d['delivery_time_in_days'] for d in details_data)
            offer.save()

        offer.details.set(created_details, bulk=False)
        offer_serialized = OfferListSerializer(offer, context=self.context)
        return offer_serialized.data
