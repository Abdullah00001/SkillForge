from django.db import models
from django.contrib.auth.models import User
from order.constants import ORDER_STATUS

# Create your models here.


class Order(models.Model):
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE,related_name='freelancer_orders')
    client = models.ForeignKey(User, on_delete=models.CASCADE,related_name='client_orders')
    order_amount = models.IntegerField(default=0)
    delivery_date = models.DateField()
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS)
    post_title = models.CharField(max_length=500)
