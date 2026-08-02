from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "order",
        "payment_method",
        "status",
        "amount",
        "transaction_id",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "transaction_id",
        "user__username",
        "order__id",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "transaction_id",
        "created_at",
    )