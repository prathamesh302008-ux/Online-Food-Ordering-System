from django.db import models
from restaurants.models import Restaurant


class Category(models.Model):

    name = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Food(models.Model):

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="foods"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="foods"
    )

    name = models.CharField(max_length=150)

    image = models.ImageField(
        upload_to="foods/",
        blank=True,
        null=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    preparation_time = models.PositiveIntegerField(
        default=20,
        help_text="Time in Minutes"
    )

    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Food"
        verbose_name_plural = "Foods"

    def __str__(self):
        return self.name