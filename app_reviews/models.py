from django.db import models
from django.conf import settings


class Review(models.Model):
    business_user = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    reviewer = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    rating = models.IntegerField(default=0)
    description = models.CharField(max_length=1024, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
