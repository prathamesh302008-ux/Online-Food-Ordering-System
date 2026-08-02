from django.db import models


class Restaurant(models.Model):

    name = models.CharField(max_length=150)

    logo = models.ImageField(
        upload_to="restaurants/logos/",
        blank=True,
        null=True
    )

    cover_image = models.ImageField(
        upload_to="restaurants/covers/",
        blank=True,
        null=True
    )

    description = models.TextField()

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    opening_time = models.TimeField()

    closing_time = models.TimeField()

    # ⭐ New Fields
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.5
    )

    delivery_time = models.PositiveIntegerField(
        default=30,
        help_text="Minutes"
    )

    delivery_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=40
    )

    minimum_order = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=100
    )

    cuisine = models.CharField(
        max_length=200,
        help_text="Example: Pizza, Burger, Chinese"
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name