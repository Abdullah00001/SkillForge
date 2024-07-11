from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404
from django.db import transaction
from transaction.serializers import TransactionSerializer
from transaction.models import Transaction
from transaction.constants import DEPOSIT, WITHDRAW, PAYMENT, RECEIVE
from order.models import Order
from order.serializers import OrderSerializer
from order.constants import SUBMITTED, COMPLETED

# Create your views here.


class DepositView(APIView):

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                profile = request.user.client_account
            except profile.DoesNotExist:
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                profile.user_balance += serializer.validated_data["transaction_amount"]
                profile.save()
                transaction = Transaction(
                    user=request.user,
                    transaction_amount=serializer.validated_data["transaction_amount"],
                    card_number=serializer.validated_data["card_number"],
                    transaction_type=DEPOSIT,
                )
                transaction.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawView(APIView):

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                profile = request.user.freelancer_account
            except profile.DoesNotExist:
                return Response(
                    {"error": "Client profile not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            profile_balance = profile.user_balance
            requested_amount = serializer.validated_data["transaction_amount"]
            if requested_amount <= profile_balance:
                try:
                    profile_balance -= requested_amount
                    profile.save()

                    transaction = Transaction(
                        user=request.user,
                        transaction_amount=serializer.validated_data[
                            "transaction_amount"
                        ],
                        card_number=serializer.validated_data["card_number"],
                        transaction_type=WITHDRAW,
                    )
                    transaction.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                except Exception as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            else:
                return Response(
                    {"error": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):

    def get_object(self, order_id):
        return get_object_or_404(Order, id=order_id)

    def put(self, request, order_id):
        order = self.get_object(order_id)

        if order.order_status != SUBMITTED:
            return Response(
                {"error": "Order is not submitted"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                amount = order.order_amount
                freelancer = order.freelancer.freelancer_account
                client = order.client.client_account

                if client.user_balance < amount:
                    return Response(
                        {"error": "Insufficient client balance."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # transaction logic
                freelancer.user_balance += amount
                client.user_balance -= amount

                # change the order status
                order.order_status = COMPLETED
                order.save()

                # create transaction model object for track history
                payment_transaction_object = Transaction.objects.create(
                    user=request.user,
                    transaction_amount=amount,
                    transaction_type=PAYMENT,
                )
                receive_transaction_object = Transaction.objects.create(
                    user=order.freelancer,
                    transaction_amount=amount,
                    transaction_type=RECEIVE,
                )
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TransactionListView(APIView):

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
