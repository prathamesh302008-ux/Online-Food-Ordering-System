from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart
from menu.models import Food


@login_required(login_url='login')
def cart_view(request):
    """Display shopping cart"""
    cart_items = Cart.objects.filter(user=request.user)
    
    total = 0
    subtotal = 0
    
    for item in cart_items:
        subtotal += item.total_price
    
    # Calculate totals (in real app, would include delivery charges, taxes)
    total = subtotal
    
    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "total": total,
        "cart_count": len(cart_items),
    }

    return render(request, "cart/cart.html", context)


@login_required(login_url='login')
def add_to_cart(request, food_id):
    """Add item to cart"""
    food = get_object_or_404(Food, id=food_id)
    
    if not food.available:
        messages.warning(request, f"{food.name} is not available right now.")
        return redirect(request.META.get('HTTP_REFERER', 'cart'))
    
    quantity = request.POST.get('quantity', 1)
    
    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food
    )
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    
    messages.success(request, f"{food.name} added to cart!")
    
    # Return JSON if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'message': f'{food.name} added to cart!',
            'cart_count': cart_count,
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required(login_url='login')
def remove_from_cart(request, cart_id):
    """Remove item from cart"""
    cart = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )
    
    food_name = cart.food.name
    cart.delete()
    
    messages.info(request, f"{food_name} removed from cart.")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = Cart.objects.filter(user=request.user).count()
        return JsonResponse({
            'success': True,
            'message': f'{food_name} removed from cart.',
            'cart_count': cart_count,
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required(login_url='login')
def increase_quantity(request, cart_id):
    """Increase item quantity in cart"""
    cart = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    cart.quantity += 1
    cart.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'quantity': cart.quantity,
            'total_price': float(cart.total_price),
        })

    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required(login_url='login')
def decrease_quantity(request, cart_id):
    """Decrease item quantity in cart"""
    cart = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'quantity': cart.quantity if cart.id else 0,
            'total_price': float(cart.total_price) if cart.id else 0,
        })

    return redirect(request.META.get('HTTP_REFERER', 'cart'))


@login_required(login_url='login')
def empty_cart(request):
    """Empty entire cart"""
    Cart.objects.filter(user=request.user).delete()
    messages.info(request, "Your cart has been emptied.")
    return redirect('cart')