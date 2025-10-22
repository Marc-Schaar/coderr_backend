from rest_framework import serializers
from app_reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'id',
            'reviewer',
            'business_user',
            'rating',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'reviewer',
            'created_at',
            'updated_at']


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'business_user',
            'reviewer',
            'created_at',
            'updated_at']

    def validate(self, data):
        for field in self.Meta.read_only_fields:
            if field in self.initial_data:
                raise serializers.ValidationError(
                    {field: "Dieses Feld darf nicht geändert werden."}
                )

        if not data:
            raise serializers.ValidationError(
                "Mindestens ein Feld muss zum Aktualisieren angegeben werden."
            )

        return data
