from django.db import models


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    # category_image = models.URLField()
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.category_name
