from django.db import models
from django.contrib.auth.models import User
from menu.models import Food


class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name="cart_food"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = [
            "-created_at"
        ]

        unique_together = (
            "user",
            "food",
        )

    @property
    def total_price(self):

        if self.food.discount_price:

            return self.food.discount_price * self.quantity

        return self.food.price * self.quantity

    def __str__(self):

        return f"{self.user.username} - {self.food.name}"