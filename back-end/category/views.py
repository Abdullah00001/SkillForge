from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from category.models import Category
from category.serializers import CategorySerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class CategoryListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            categories = Category.objects.all()
            if not categories.exists():
                return Response(
                    {"error": "No categories found."}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Categories do not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
