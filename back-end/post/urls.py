from django.urls import path
from post.views import PostView, PostDetailView, PostListView

urlpatterns = [
    path("create-post/", PostView.as_view()),
    path("post-details/<int:pk>/", PostDetailView.as_view()),
    path("post-list/", PostListView.as_view(), name="post-list"),
]
