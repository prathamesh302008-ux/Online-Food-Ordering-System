from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from orders.models import Order
from .models import Payment


@login_required(login_url="login")
def payment_page(request):

    order = Order.objects.filter(
        user=request.user,
        payment_status="Pending"
    ).order_by("-id").first()

    if not order:
        messages.warning(request, "No pending order found.")
        return redirect("home")

    if request.method == "POST":

        payment_method = request.POST.get("payment_method")

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "user": request.user,
                "amount": order.total_price,
                "payment_method": payment_method,
                "status": "Success",
            }
        )

        if not created:
            payment.user = request.user
            payment.payment_method = payment_method
            payment.amount = order.total_price
            payment.status = "Success"
            payment.save()

        order.payment_status = "Paid"
        order.payment_method = payment_method
        order.status = "Confirmed"
        order.save()

        messages.success(request, "Payment Successful.")
        return redirect("payment_success")

    return render(
        request,
        "payments/payment.html",
        {
            "order": order,
        },
    )


@login_required(login_url="login")
def payment_success(request):
    return render(
        request,
        "payments/payment_success.html"
    )