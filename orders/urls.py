from django.urls import path
from . import views

urlpatterns = [

    # My Orders
    path(
        "",
        views.my_orders,
        name="my_orders",
    ),

    # Order Details
    path(
        "<int:order_id>/",
        views.order_detail,
        name="order_detail",
    ),

    # Cancel Single Order
    path(
        "<int:order_id>/cancel/",
        views.cancel_order,
        name="cancel_order",
    ),

    # Cancel All Orders
    path(
        "cancel-all/",
        views.cancel_all_orders,
        name="cancel_all_orders",
    ),

    # Track Order
    path(
        "<int:order_id>/track/",
        views.track_order,
        name="track_order",
    ),
]