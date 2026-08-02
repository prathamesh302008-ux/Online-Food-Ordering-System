import uuid

from django.db import models
from django.contrib.auth.models import User
from orders.models import Order


class Payment(models.Model):

    PAYMENT_METHODS = [
        ("COD", "Cash On Delivery"),
        ("UPI", "UPI"),
        ("Google Pay", "Google Pay"),
        ("PhonePe", "PhonePe"),
        ("Paytm", "Paytm"),
        ("Credit Card", "Credit Card"),
        ("Debit Card", "Debit Card"),
        ("Net Banking", "Net Banking"),
    ]

    STATUS = [
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
        default="COD"
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        editable=False
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = "TXN-" + uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_id