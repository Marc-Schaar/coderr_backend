from rest_framework import serializers
from app_accounts.models import User
from app_offers.models import Offer, OfferDetails
from app_accounts.api.serializers import UserListSerializer


class OfferDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetails
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # details = OfferDetailsSerializer(many=True)
    details = serializers.SerializerMethodField()
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

    def get_details(self, obj):
        request = self.context.get('request')
        details = obj.details.all()

        return [
            {
                "id": d.id,
                "url": request.build_absolute_uri(f"/api/offerdetails/{d.id}/")
            }
            for d in details
        ]


class OfferCreateSerializer(serializers.ModelSerializer):
    details = OfferDetailsSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details',
        ]

    def validate(self, attrs):
        details = attrs.get('details', [])
        if len(details) < 3:
            raise serializers.ValidationError("At least three offer detail is required.")
        return attrs

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
        return offer


class OfferDetailSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'details',
            'created_at',
            'updated_at',
            'min_price',
            'min_delivery_time',
        ]

    def get_details(self, obj):
        request = self.context.get('request')
        details = obj.details.all()

        return [
            {
                "id": d.id,
                "url": request.build_absolute_uri(f"/api/offerdetails/{d.id}/")
            }
            for d in details
        ]
