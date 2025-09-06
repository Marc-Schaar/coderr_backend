from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TYPE_CHOICES = [("customer", "Customer"), ("business", "Business")]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)