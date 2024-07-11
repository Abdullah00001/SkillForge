from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user_opinions.serializers import ReviewSerializer
from order.models import Order
from django.shortcuts import get_object_or_404
from user_opinions.models import Review

# Create your views here.


class ReviewCreateView(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if request.user != order.client:
            return Response(
                {"error": "You are not authorized to review this order."},
                status=status.HTTP_403_FORBIDDEN,
            )

        freelancer = order.freelancer
        client = request.user
        ratings = request.data.get("ratings")
        description = request.data.get("description")

        data = {
            "client": client,
            "freelancer": freelancer,
            "order": order,
            "ratings": ratings,
            "description": description,
        }

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListView(APIView):
    def get(self, request):
        try:
            reviews = Review.objects.all()
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
