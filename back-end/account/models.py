from django.db import models
from django.contrib.auth.models import User
from account.constants import ACCOUNT_TYPE, GENDER_TYPE, LANGUAGES
from category.models import Category
from skills.models import Skills

# Create your models here.


class FreelancerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="freelancer_account"
    )
    profile_image = models.URLField()
    profile_title = models.CharField(max_length=350)
    profole_category = models.CharField(max_length=230)
    contact_number = models.CharField(max_length=15)
    gender_type = models.CharField(max_length=15, choices=GENDER_TYPE)
    user_role = models.CharField(max_length=120)
    user_skill = models.ManyToManyField(Skills)
    user_country = models.CharField(max_length=180)
    user_address = models.CharField(max_length=750)
    languages = models.CharField(max_length=40, choices=LANGUAGES)
    user_education = models.TextField()
    user_balance = models.IntegerField(default=0)
    user_description = models.TextField()
    account_type = models.CharField(max_length=70, choices=ACCOUNT_TYPE)

    def __str__(self) -> str:
        return f"{self.user.username} {self.account_type}"


class ClientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="client_account"
    )
    profile_image = models.URLField()
    contact_number = models.CharField(max_length=15)
    gender_type = models.CharField(max_length=15, choices=GENDER_TYPE)
    user_role = models.CharField(max_length=120)
    user_country = models.CharField(max_length=180)
    user_address = models.CharField(max_length=750)
    languages = models.CharField(max_length=40, choices=LANGUAGES)
    user_balance = models.IntegerField(default=0)
    user_description = models.TextField()

    def __str__(self) -> str:
        return f"{self.user.username} {self.account_type}"
