from django.urls import path
from order.views import (
    CreateOrderView,
    OrderListView,
    OrderDetailsView,
    SubmitOrderView,
)

urlpatterns = [
    path(
        "create-order/<int:proposal_id>/",
        CreateOrderView.as_view(),
        name="create-order",
    ),
    path(
        "order-list/",
        OrderListView.as_view(),
        name="order-list",
    ),
    path(
        "order-details/<int:order_id>/", OrderDetailsView.as_view(), name="order-detail"
    ),
    path("submit-order/<int:order_id>/", SubmitOrderView.as_view(), name="submit-file"),
]
