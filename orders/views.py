from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

from .models import Order


@login_required(login_url="login")
def my_orders(request):
    """Display user's orders"""

    orders_list = Order.objects.filter(
        user=request.user
    ).prefetch_related("items")

    status_filter = request.GET.get("status")

    if status_filter:
        orders_list = orders_list.filter(
            status=status_filter
        )

    paginator = Paginator(
        orders_list,
        10
    )

    page = request.GET.get("page")

    try:
        orders = paginator.page(page)

    except PageNotAnInteger:
        orders = paginator.page(1)

    except EmptyPage:
        orders = paginator.page(
            paginator.num_pages
        )

    context = {
        "orders": orders,
        "status_choices": Order.STATUS,
        "selected_status": status_filter,
    }

    return render(
        request,
        "orders/my_orders.html",
        context,
    )


@login_required(login_url="login")
def order_detail(request, order_id):
    """Display Order Details"""

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    order_items = order.items.select_related(
        "food"
    )

    subtotal = sum(
        item.total_price
        for item in order_items
    )

    context = {
        "order": order,
        "order_items": order_items,
        "subtotal": subtotal,
        "delivery_charge": order.delivery_charge,
        "discount_amount": order.discount_amount,
        "total": order.total_price,
    }

    return render(
        request,
        "orders/order_detail.html",
        context,
    )


@login_required(login_url="login")
def cancel_order(request, order_id):
    """Cancel Single Order"""

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    if order.status in [
        "Delivered",
        "Cancelled",
    ]:

        messages.error(
            request,
            "This order cannot be cancelled."
        )

        return redirect(
            "order_detail",
            order_id=order.id,
        )

    if request.method == "POST":

        order.status = "Cancelled"
        order.save()

        messages.success(
            request,
            "Order cancelled successfully."
        )

        return redirect(
            "order_detail",
            order_id=order.id,
        )

    return render(
        request,
        "orders/cancel_order.html",
        {
            "order": order,
        },
    )


@login_required(login_url="login")
@require_POST
def cancel_all_orders(request):
    """Cancel All Active Orders"""

    active_orders = Order.objects.filter(
        user=request.user
    ).exclude(
        status__in=[
            "Delivered",
            "Cancelled",
        ]
    )

    total = active_orders.count()

    if total == 0:

        messages.warning(
            request,
            "No active orders available."
        )

        return redirect("my_orders")

    active_orders.update(
        status="Cancelled"
    )

    messages.success(
        request,
        f"{total} order(s) cancelled successfully."
    )

    return redirect(
        "my_orders"
    )


@login_required(login_url="login")
def track_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    status_timeline = [
        "Pending",
        "Confirmed",
        "Preparing",
        "Out For Delivery",
        "Delivered",
    ]

    context = {
        "order": order,
        "status_timeline": status_timeline,
    }

    return render(
        request,
        "orders/track_order.html",
        context,
    )