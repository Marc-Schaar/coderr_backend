import django_filters
from rest_framework import serializers
from app_offers.models import Offer
from app_accounts.models import User


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(method='filter_creator_id')
    min_price = django_filters.NumberFilter(field_name="min_price", lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name="min_delivery_time", lookup_expr='lte')

    class Meta:
        model = Offer
        fields = []

    def filter_creator_id(self, queryset, name, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError({"creator_id": "User does not exist."})
        return queryset.filter(user_id=value)
