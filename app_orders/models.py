from django.db import models
from app_accounts.models import User


class Order(models.Model):
    OFFER_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer_user = models.ForeignKey(User, related_name='customer_orders',
                                      on_delete=models.CASCADE,  null=True, blank=True)
    business_user = models.ForeignKey(User, related_name='business_orders',
                                      on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=False)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField(null=True)
    price = models.IntegerField()
    features = models.JSONField(null=True, blank=True)
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPE_CHOICES, default='basic')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
