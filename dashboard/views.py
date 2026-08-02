from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from orders.models import Order
from payments.models import Payment


@login_required(login_url="login")
def dashboard_view(request):
    """Simple dashboard overview for authenticated users."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")[:5]
    payments = Payment.objects.filter(order__user=request.user).order_by("-created_at")[:5]

    total_spent = Order.objects.filter(user=request.user).aggregate(total=Sum("total_price"))["total"] or 0
    total_orders = Order.objects.filter(user=request.user).count()

    context = {
        "orders": orders,
        "payments": payments,
        "total_spent": total_spent,
        "total_orders": total_orders,
    }
    return render(request, "dashboard/dashboard.html", context)
