from django.db import models
from app_accounts.models import User


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=100)
    image = models.ImageField(upload_to="offers_img", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.IntegerField(blank=False, default=0)
    min_delivery_time = models.IntegerField(blank=False, default=0)

    def __str__(self):
        return self.title


class OfferDetails(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(blank=False, max_length=100)
    revisions = models.IntegerField(blank=False)
    delivery_time_in_days = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)
    features = models.JSONField(blank=False)
    offer_type = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.title
