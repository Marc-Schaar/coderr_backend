from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TYPE_CHOICES = [("customer", "Customer"), ("business", "Business")]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    file= models.FileField(upload_to='user_files/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    tel= models.CharField(max_length=15, blank=True)
    description = models.CharField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
