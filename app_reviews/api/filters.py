import django_filters
from app_reviews.models import Review


class ReviewFilter(django_filters.FilterSet):
    """
    FilterSet for filtering reviews by business user and reviewer.
    Allows filtering reviews based on business_user_id and reviewer_id.
    """
    business_user_id = django_filters.NumberFilter(field_name="business_user_id")
    reviewer_id = django_filters.NumberFilter(field_name="reviewer_id")

    class Meta:
        model = Review
        fields = []
