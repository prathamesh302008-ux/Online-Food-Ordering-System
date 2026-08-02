from django.shortcuts import render, get_object_or_404
from .models import Restaurant


def restaurant_list(request):
    """
    Restaurant Listing Page
    """

    restaurants = Restaurant.objects.filter(
        is_active=True
    ).order_by(
        "-is_featured",
        "-rating",
        "name"
    )

    search = request.GET.get("search")

    if search:
        restaurants = restaurants.filter(
            name__icontains=search
        )

    context = {
        "restaurants": restaurants,
        "search": search,
    }

    return render(
        request,
        "restaurants/restaurant_list.html",
        context,
    )


def restaurant_detail(request, pk):
    """
    Restaurant Detail Page
    """

    restaurant = get_object_or_404(
        Restaurant,
        pk=pk,
        is_active=True,
    )

    context = {
        "restaurant": restaurant,
    }

    return render(
        request,
        "restaurants/restaurant_detail.html",
        context,
    )