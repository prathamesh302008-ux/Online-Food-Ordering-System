from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("add/<int:food_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:cart_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("increase/<int:cart_id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:cart_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("empty/", views.empty_cart, name="empty_cart"),
]