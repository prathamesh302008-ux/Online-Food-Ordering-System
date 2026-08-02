from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "city",
        "phone",
        "rating",
        "delivery_time",
        "delivery_fee",
        "minimum_order",
        "is_featured",
        "is_active",
        "created_at",
    )

    list_filter = (
        "city",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "name",
        "city",
        "phone",
        "email",
        "cuisine",
    )

    ordering = (
        "name",
    )

    list_editable = (
        "is_featured",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )