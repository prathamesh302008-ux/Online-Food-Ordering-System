from django.db import models
from django.contrib.auth.models import User
from menu.models import Food


class Review(models.Model):

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
    )

    review = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "food")

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"