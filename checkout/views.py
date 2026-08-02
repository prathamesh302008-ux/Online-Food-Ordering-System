from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction

from cart.models import Cart
from orders.models import Order, OrderItem
from payments.models import Payment

from .models import DeliveryAddress, OrderCheckout
from .forms import (
    DeliveryAddressForm,
    CheckoutForm,
    QuickCheckoutForm,
)


@login_required(login_url="login")
def checkout(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related("food")

    if not cart_items.exists():
        messages.warning(
            request,
            "Your cart is empty."
        )
        return redirect("cart")

    subtotal = sum(
        item.total_price
        for item in cart_items
    )

    delivery_charge = 50

    discount = 0

    total = subtotal + delivery_charge - discount

    addresses = DeliveryAddress.objects.filter(
        user=request.user
    )

    context = {
        "cart_items": cart_items,
        "addresses": addresses,
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "discount": discount,
        "total": total,
    }

    return render(
        request,
        "checkout/checkout.html",
        context,
    )


@login_required(login_url="login")
def add_delivery_address(request):

    if request.method == "POST":

        form = DeliveryAddressForm(request.POST)

        if form.is_valid():

            address = form.save(commit=False)

            address.user = request.user

            if address.is_default:

                DeliveryAddress.objects.filter(
                    user=request.user
                ).update(
                    is_default=False
                )

            address.save()

            messages.success(
                request,
                "Address added successfully."
            )

            return redirect("checkout")

    else:

        form = DeliveryAddressForm()

    return render(
        request,
        "checkout/add_address.html",
        {
            "form": form,
        },
    )


@login_required(login_url="login")
def edit_delivery_address(request, address_id):

    address = get_object_or_404(
        DeliveryAddress,
        id=address_id,
        user=request.user,
    )

    if request.method == "POST":

        form = DeliveryAddressForm(
            request.POST,
            instance=address,
        )

        if form.is_valid():

            address = form.save(commit=False)

            if address.is_default:

                DeliveryAddress.objects.filter(
                    user=request.user
                ).exclude(
                    id=address.id
                ).update(
                    is_default=False
                )

            address.save()

            messages.success(
                request,
                "Address updated successfully."
            )

            return redirect("checkout")

    else:

        form = DeliveryAddressForm(
            instance=address
        )

    return render(
        request,
        "checkout/edit_address.html",
        {
            "form": form,
            "address": address,
        },
    )

@login_required(login_url="login")
@require_http_methods(["POST"])
def place_order(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related("food")

    if not cart_items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("cart")

    address_id = request.POST.get(
        "address_id"
    )

    payment_method = request.POST.get(
        "payment_method"
    )

    special_instructions = request.POST.get(
        "special_instructions",
        "",
    )

    if not address_id:

        messages.error(
            request,
            "Please select a delivery address."
        )

        return redirect("checkout")

    address = get_object_or_404(
        DeliveryAddress,
        id=address_id,
        user=request.user,
    )

    valid_methods = [
        "COD",
        "UPI",
        "Google Pay",
        "PhonePe",
        "Paytm",
        "Credit Card",
        "Debit Card",
        "Net Banking",
    ]

    if payment_method not in valid_methods:

        messages.error(
            request,
            "Invalid payment method."
        )

        return redirect("checkout")

    subtotal = sum(
        item.total_price
        for item in cart_items
    )

    delivery_charge = 50

    discount = 0

    total = subtotal + delivery_charge - discount

    try:

        with transaction.atomic():

            order = Order.objects.create(

                user=request.user,

                total_price=total,

                status="Pending",

                payment_status="Pending",

                payment_method=payment_method,

                delivery_address=(
                    f"{address.address_line1}, "
                    f"{address.address_line2 or ''}, "
                    f"{address.city}, "
                    f"{address.state} - "
                    f"{address.pincode}"
                ),

                phone=address.phone,

                email=address.email,

                delivery_charge=delivery_charge,

                discount_amount=discount,

                special_instructions=special_instructions,

            )

            for item in cart_items:

                OrderItem.objects.create(

                    order=order,

                    food=item.food,

                    quantity=item.quantity,

                    price=item.food.discount_price
                    if item.food.discount_price
                    else item.food.price,

                )

            Payment.objects.create(

                user=request.user,

                order=order,

                payment_method=payment_method,

                amount=total,

                status=(
                    "Success"
                    if payment_method == "COD"
                    else "Pending"
                ),

            )

            OrderCheckout.objects.create(

                order=order,

                delivery_address=address,

                special_instructions=special_instructions,

                discount_amount=discount,

                delivery_charge=delivery_charge,

            )

            cart_items.delete()

            if payment_method == "COD":

                order.payment_status = "Paid"

                order.status = "Confirmed"

                order.save()

            messages.success(
                request,
                "Order placed successfully."
            )

            return redirect(
                "order_success",
                order_id=order.id,
            )

    except Exception as e:

        messages.error(
            request,
            str(e),
        )

        return redirect("checkout")


@login_required(login_url="login")
def order_success(request, order_id):

    order = get_object_or_404(

        Order,

        id=order_id,

        user=request.user,

    )

    order_items = order.items.select_related(
        "food"
    )

    subtotal = sum(

        item.price * item.quantity

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

        "checkout/order_success.html",

        context,

    )