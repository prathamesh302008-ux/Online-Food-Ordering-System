from django.contrib import admin
from .models import DeliveryAddress, OrderCheckout


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "city",
        "is_default",
        "created_at",
    )
    
    list_filter = (
        "is_default",
        "city",
        "created_at",
    )
    
    search_fields = (
        "user__username",
        "full_name",
        "phone",
        "city",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(OrderCheckout)
class OrderCheckoutAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "coupon_code",
        "discount_amount",
        "delivery_charge",
        "created_at",
    )
    
    list_filter = (
        "created_at",
    )
    
    search_fields = (
        "order__id",
        "coupon_code",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at",
    )
