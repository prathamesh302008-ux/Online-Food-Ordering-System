from django.db import models
from django.contrib.auth.models import User
from menu.models import Food


class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "food",
        )

    def __str__(self):
        return self.food.name