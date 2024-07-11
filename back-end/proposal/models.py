from django.db import models
from post.models import Post
from django.contrib.auth.models import User
from proposal.constants import PROPOSAL_STATUS

# Create your models here.


class Proposal(models.Model):
    freelancer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="freelancer_proposals"
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="client_proposals"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    proposal_amount = models.IntegerField(default=0)
    delivered_in = models.IntegerField(default=0)
    description = models.TextField()
    proposal_status = models.CharField(max_length=100, choices=PROPOSAL_STATUS)
