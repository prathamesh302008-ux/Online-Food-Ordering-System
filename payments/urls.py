from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_page, name="payment"),
    path("success/", views.payment_success, name="payment_success"),
]