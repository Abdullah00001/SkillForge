from django.urls import path
from proposal.views import (
    ProposalCreateView,
    ProposalListView,
    ProposalDetailView,
    ProposalRejectView,
    FreelancerProposalsView,
)

urlpatterns = [
    path(
        "create-proposal/<int:post_id>/",
        ProposalCreateView.as_view(),
        name="create_proposal",
    ),
    path(
        "client/proposal-list/",
        ProposalListView.as_view(),
        name="proposals_list",
    ),
    path(
        "client/proposal-details/<int:proposal_id>/",
        ProposalDetailView.as_view(),
        name="detail-proposal",
    ),
    path(
        "client/reject-proposal/<int:proposal_id>/",
        ProposalRejectView.as_view(),
        name="proposal-reject",
    ),
    path(
        "freelancer/proposals/",
        FreelancerProposalsView.as_view(),
        name="freelancer-proposals",
    ),
]
