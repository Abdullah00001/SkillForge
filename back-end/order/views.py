from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import EmailMessage
from datetime import datetime, timedelta
from order.serializers import OrderSerializer
from proposal.models import Proposal
from order.models import Order
from order.constants import RUNNING, SUBMITTED, COMPLETED

# Create your views here.


class CreateOrderView(APIView):

    def post(self, request, proposal_id):
        try:
            proposal = Proposal.objects.get(id=proposal_id)
        except Proposal.DoesNotExist:
            return Response(
                {"error": "Proposal not found"}, status=status.HTTP_404_NOT_FOUND
            )
        freelancer = proposal.freelancer
        client = proposal.client
        proposal_amount = proposal.proposal_amount
        post_title = proposal.post.post_title
        delivery_days = proposal.delivered_in
        today = datetime.now().date()
        delivery_date = today + timedelta(days=delivery_days)

        order_data = {
            "freelancer": freelancer,
            "client": client,
            "order_amount": proposal_amount,
            "delivery_date": delivery_date,
            "order_status": RUNNING,
            "post_title": post_title,
        }
        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetailsView(APIView):
    def get(self, request, order_id, format=None):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class SubmitOrderView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if order.freelancer != request.user:
            return Response(
                {"error": "You are not authorized to submit this order"},
                status=status.HTTP_403_FORBIDDEN,
            )
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        if file.size > 5 * 1024 * 1024:
            return Response(
                {"error": "File too large"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not file.name.endswith(".zip"):
            return Response(
                {"error": "Invalid file type. Only .zip files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        email = EmailMessage(
            subject=f"Order {order.id} - Submission",
            body=f"Dear {order.client.username},\n\nThe freelancer has submitted the completed task for the order {order.id}. Please find the attached file.\n\nBest regards,\nSkillForge",
            to=[order.client.email],
        )
        email.attach(file.name, file.read(), file.content_type)
        try:
            email.send()
            order.order_status = SUBMITTED
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
