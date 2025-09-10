from django.db import models
from app_accounts.models import User 

 
class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="offers_img", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    details = models.JSONField(null= True, blank=True)
    min_price = models.IntegerField()
    min_delivery_time = models.IntegerField()
     

    def __str__(self):
         return self.title

