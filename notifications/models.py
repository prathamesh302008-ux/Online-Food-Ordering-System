from django.db import models
from django.contrib.auth.models import User
from orders.models import Order


class Notification(models.Model):
    """
    Notification model for tracking notifications to users.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('Order', 'Order Status'),
        ('Promotion', 'Promotion'),
        ('Alert', 'Alert'),
        ('Message', 'Message'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    
    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='Message'
    )
    
    title = models.CharField(max_length=200)
    
    message = models.TextField()
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
    )
    
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
