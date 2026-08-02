from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("add-address/", views.add_delivery_address, name="add_address"),
    path("edit-address/<int:address_id>/", views.edit_delivery_address, name="edit_address"),
    path("place-order/", views.place_order, name="place_order"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
]