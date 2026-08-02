from django.db import models
from django.contrib.auth.models import User
from menu.models import Food


class Order(models.Model):

    STATUS = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Preparing", "Preparing"),
        ("Out For Delivery", "Out For Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    ]

    PAYMENT_METHOD = [
        ("UPI", "UPI"),
        ("Google Pay", "Google Pay"),
        ("PhonePe", "PhonePe"),
        ("Paytm", "Paytm"),
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
        ("Net Banking", "Net Banking"),
        ("Cash On Delivery", "Cash On Delivery"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default="Pending"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD,
        blank=True,
        null=True
    )

    delivery_address = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    coupon_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    special_instructions = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.food.name} x {self.quantity}"