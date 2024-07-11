from rest_framework import serializers
from proposal.models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            "id",
            "freelancer",
            "client",
            "post",
            "proposal_amount",
            "delivered_in",
            "description",
            "proposal_status",
        ]
