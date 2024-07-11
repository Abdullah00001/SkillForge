from django.db import models
from category.models import Category
from skills.models import Skills
from post.constants import POST_STATUS
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=150)
    post_description = models.TextField()
    post_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget = models.IntegerField(default=0)
    deadline = models.DateField()
    required_skill = models.ManyToManyField(Skills)
    post_creation_time = models.DateTimeField(auto_now_add=True)
    post_status = models.CharField(max_length=80, choices=POST_STATUS)