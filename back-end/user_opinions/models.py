from django.db import models
from django.contrib.auth.models import User
from user_opinions.constants import USER_RATING
from order.models import Order

# Create your models here.


class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_reviews")
    freelancer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="freelancer_reviews"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_reviews")
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = models.CharField(max_length=120, choices=USER_RATING)
    description = models.TextField()
