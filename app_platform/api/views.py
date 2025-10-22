from app_offers.models import Offer
from app_accounts.models import User
from app_reviews.models import Review
from django.db import models
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg


class BaseInfoView(APIView):
    def get(self, request):
        review_count = Review.objects.count()
        avg = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0
        business_profile_count = User.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": round(avg, 1),
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }

        return Response(data, status=status.HTTP_200_OK)
