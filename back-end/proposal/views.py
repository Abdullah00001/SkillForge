from django.shortcuts import render
from proposal.serializers import ProposalSerializer
from proposal.models import Proposal
from post.models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from proposal.constants import PENDING, REJECTED
from rest_framework.exceptions import NotFound

# Create your views here.


class ProposalCreateView(generics.CreateAPIView):
    serializer_class = ProposalSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        post = Post.objects.get(id=post_id)
        client = post.user
        freelancer = self.request.user
        serializer.save(
            freelancer=freelancer,
            client=client,
            post=post,
            proposal_status=PENDING,
        )

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs["post_id"]
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return super().create(request, *args, **kwargs)


class ProposalListView(generics.ListAPIView):
    serializer_class = ProposalSerializer

    def get_queryset(self):
        client = self.request.user
        return Proposal.objects.filter(client=client, proposal_status=PENDING)


class ProposalDetailView(generics.RetrieveAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    lookup_url_kwarg = "proposal_id"

    def retrieve(self, request, *args, **kwargs):
        proposal_id = kwargs.get(self.lookup_url_kwarg)
        try:
            proposal = self.get_object()
        except Proposal.DoesNotExist:
            raise NotFound(detail="Proposal not found")

        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=status.HTTP_200_ok)


class ProposalRejectView(generics.UpdateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    lookup_url_kwarg = "proposal_id"

    def patch(self, request, *args, **kwargs):
        try:
            proposal = self.get_object()
        except Proposal.DoesNotExist:
            raise NotFound(detail="Proposal not found")
        proposal.proposal_status = REJECTED
        proposal.save()
        serializer = self.get_serializer(proposal)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FreelancerProposalsView(generics.ListAPIView):
    serializer_class = ProposalSerializer

    def get_queryset(self):
        freelancer = self.request.user
        return Proposal.objects.filter(freelancer=freelancer)
