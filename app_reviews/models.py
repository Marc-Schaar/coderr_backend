from django.db import models
from app_accounts.models import User


class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    rating = models.IntegerField(blank=False)
    description = models.CharField(max_length=1024, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
