from django.contrib import admin
from .models import Category, Food


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "image",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "restaurant",
        "category",
        "price",
        "discount_price",
        "preparation_time",
        "available",
        "created_at",
    )

    list_filter = (
        "restaurant",
        "category",
        "available",
    )

    search_fields = (
        "name",
        "restaurant__name",
        "category__name",
    )

    ordering = (
        "name",
    )

    list_editable = (
        "available",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )