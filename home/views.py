from django.shortcuts import render
from django.db.models import Avg, Count

from menu.models import Category, Food
from restaurants.models import Restaurant
from reviews.models import Review
from cart.models import Cart


def home(request):
    """Home Page"""

    # Categories
    categories = Category.objects.all()[:6]

    # Popular Foods
    popular_foods = (
        Food.objects.filter(available=True)
        .select_related("category", "restaurant")
        .annotate(
            review_count=Count("reviews"),
            avg_rating=Avg("reviews__rating"),
        )
        .order_by("-review_count", "-created_at")[:8]
    )

    # Restaurants
    restaurants = Restaurant.objects.filter(is_active=True)[:6]

    # Testimonials
    testimonials = (
        Review.objects.select_related("user", "food")
        .order_by("-created_at")[:6]
    )

    # Cart Count
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    context = {
        "categories": categories,
        "popular_foods": popular_foods,
        "restaurants": restaurants,
        "testimonials": testimonials,
        "cart_count": cart_count,
    }

    return render(request, "home/index.html", context)