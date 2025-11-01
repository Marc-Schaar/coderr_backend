from rest_framework import serializers
from app_reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    Handles serialization and deserialization of review data, including all relevant fields.
    Most fields are read-only to ensure data integrity after review creation.
    """
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
    """
    Serializer for detailed review view.
    Ensures certain fields are read-only and validates that only allowed fields are updated.
    """
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
        """
        Validates that read-only fields are not updated and at least one field is provided for update.
        """
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
