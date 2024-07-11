from django.db import models
from category.models import Category


# Create your models here.
class Skills(models.Model):
    skill_name = models.CharField(max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_skill"
    )

    def __str__(self) -> str:
        return self.skill_name
