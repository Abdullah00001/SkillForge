from django.urls import path
from transaction.views import (
    DepositView,
    WithdrawView,
    PaymentView,
    TransactionListView,
)

urlpatterns = [
    path("deposit/", DepositView.as_view(), name="deposit"),
    path("withdraw/", WithdrawView.as_view(), name="withdraw"),
    path("payment/<int:order_id>/", PaymentView.as_view(), name="payment"),
    path("transactions-list/", TransactionListView.as_view(), name="transactions-list"),
]
