from django.db import models
from django.contrib.auth.models import User
from orders.models import Order


class DeliveryAddress(models.Model):
    """
    Delivery Address model for storing user delivery addresses.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='delivery_addresses'
    )
    
    full_name = models.CharField(max_length=150)
    
    phone = models.CharField(max_length=15)
    
    email = models.EmailField()
    
    address_line1 = models.CharField(max_length=255)
    
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    
    city = models.CharField(max_length=100)
    
    state = models.CharField(max_length=100)
    
    pincode = models.CharField(max_length=10)
    
    country = models.CharField(
        max_length=100,
        default='India'
    )
    
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        verbose_name = 'Delivery Address'
        verbose_name_plural = 'Delivery Addresses'
    
    def __str__(self):
        return f"{self.full_name} - {self.city}"


class OrderCheckout(models.Model):
    """
    Order Checkout model to store checkout details for orders.
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='checkout'
    )
    
    delivery_address = models.ForeignKey(
        DeliveryAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    special_instructions = models.TextField(
        blank=True,
        null=True,
        help_text="Any special delivery instructions"
    )
    
    coupon_code = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Order Checkout'
        verbose_name_plural = 'Order Checkouts'
    
    def __str__(self):
        return f"Checkout for Order #{self.order.id}"
