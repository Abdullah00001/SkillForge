from django.db import models
from django.contrib.auth.models import User
from transaction.constants import TRANSACTION_TYPE

# Create your models here.


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number=models.IntegerField()
    transaction_amount = models.IntegerField()
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)
