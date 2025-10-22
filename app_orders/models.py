from django.db import models
from app_accounts.models import User


class Order(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="offers_img", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.JSONField(null=True, blank=True)
    min_price = models.FloatField()
    min_delivery_time = models.IntegerField()

    def __str__(self):
        return self.title

    {
        "id": 1,
        "customer_user": 1,
        "business_user": 2,

        "revisions": 3,
        "delivery_time_in_days": 5,
        "price": 150,
        "features": [
            "Logo Design",
            "Visitenkarten"
        ],
        "offer_type": "basic",
        "status": "in_progress",
        "created_at": "2024-09-29T10:00:00Z",
        "updated_at": "2024-09-30T12:00:00Z"
    }
