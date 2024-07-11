from django.urls import path
from user_opinions.views import ReviewCreateView, ReviewListView

urlpatterns = [
    path("review/<int:order_id>/", ReviewCreateView.as_view(), name="create-review"),
    path("review-list/", ReviewListView.as_view(), name="review-list"),
]
