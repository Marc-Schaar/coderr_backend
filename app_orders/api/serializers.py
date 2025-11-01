from rest_framework import serializers
from app_orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    Handles serialization and deserialization of order data, including all relevant fields.
    Most fields are read-only to ensure data integrity after order creation.
    """
    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'created_at',
            'updated_at',
        ]
