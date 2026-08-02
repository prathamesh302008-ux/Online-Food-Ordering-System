from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from menu.models import Food
from .models import Wishlist


@login_required(login_url="login")
def wishlist_view(request):
    """Display the authenticated user's wishlist."""
    items = Wishlist.objects.filter(user=request.user).select_related("food")
    return render(request, "wishlist/wishlist.html", {"items": items})


@login_required(login_url="login")
def add_to_wishlist(request, food_id):
    """Add a food item to the wishlist."""
    food = get_object_or_404(Food, id=food_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, food=food)
    if created:
        messages.success(request, f"{food.name} added to your wishlist.")
    else:
        messages.info(request, f"{food.name} is already in your wishlist.")
    return redirect(request.META.get("HTTP_REFERER", "wishlist"))


@login_required(login_url="login")
def remove_from_wishlist(request, food_id):
    """Remove a food item from the wishlist."""
    wishlist_item = get_object_or_404(Wishlist, user=request.user, food_id=food_id)
    wishlist_item.delete()
    messages.info(request, "Item removed from your wishlist.")
    return redirect("wishlist")
