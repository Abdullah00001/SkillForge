from django.urls import path
from category.views import CategoryListAPIView

urlpatterns = [
    path("category-list/", CategoryListAPIView.as_view(), name="category-list"),
]
