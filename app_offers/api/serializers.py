from rest_framework import serializers
from app_accounts.models import User
from app_offers.models import Offer, OfferDetails
from app_accounts.api.serializers import UserListSerializer


class OfferDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for offer details, including title, revisions, delivery time, price, features, and offer type.
    """
    class Meta:
        model = OfferDetails
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing offers with user, details, and user details.
    Includes a method to generate detail URLs for each offer detail.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
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
        """
        Returns a list of offer detail objects with their API URLs for the given offer.
        """
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
    """
    Serializer for creating offers with nested offer details.
    Validates that at least three offer details are provided and creates related details.
    """
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
        """
        Validates that at least three offer details are provided.
        """
        details = attrs.get('details', [])
        if len(details) < 3:
            raise serializers.ValidationError("At least three offer detail is required.")
        return attrs

    def create(self, validated_data):
        """
        Creates an offer and its related offer details, updating min price and delivery time.
        """
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


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offers and their related offer details.
    Updates offer fields and synchronizes related details.
    """
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

    def update(self, instance, validated_data):
        """
        Updates the offer instance and its related offer details.
        """
        details_data = validated_data.pop('details', [])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        for detail_data in details_data:
            detail_serializer = OfferDetailsSerializer(data=detail_data)
            detail_serializer.is_valid(raise_exception=True)

        for detail_data in details_data:
            offer_type = detail_data.get("offer_type")
            detail = instance.details.get(offer_type=offer_type)
            for key, value in detail_data.items():
                setattr(detail, key, value)
            detail.save()

        if instance.details.exists():
            instance.min_price = min(d.price for d in instance.details.all())
            instance.min_delivery_time = min(d.delivery_time_in_days for d in instance.details.all())
            instance.save()
        return instance


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed offer view, including all offer fields and related details with URLs.
    """
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
        """
        Returns a list of offer detail objects with their API URLs for the given offer.
        """
        request = self.context.get('request')
        details = obj.details.all()

        return [
            {
                "id": d.id,
                "url": request.build_absolute_uri(f"/api/offerdetails/{d.id}/")
            }
            for d in details
        ]
