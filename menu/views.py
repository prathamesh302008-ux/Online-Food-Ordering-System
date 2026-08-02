from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg
from .models import Food, Category
from .forms import FoodSearchForm
from reviews.models import Review
from cart.models import Cart


def menu(request):
    foods_list = (
        Food.objects.filter(available=True)
        .select_related("restaurant", "category")
    )

    categories = Category.objects.all()
    form = FoodSearchForm(request.GET)

    search_query = request.GET.get("search_query", "")
    if search_query:
        foods_list = foods_list.filter(
            Q(name__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(restaurant__name__icontains=search_query)
        )

    category_id = request.GET.get("category")
    if category_id:
        foods_list = foods_list.filter(category_id=category_id)

    sort_by = request.GET.get("sort_by", "-created_at")
    foods_list = foods_list.order_by(sort_by)

    paginator = Paginator(foods_list, 12)
    page = request.GET.get("page")

    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    return render(
        request,
        "menu/menu.html",
        {
            "foods": foods,
            "categories": categories,
            "form": form,
            "search_query": search_query,
            "cart_count": cart_count,
            "paginator": paginator,
        },
    )


def category_foods(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    foods_list = (
        Food.objects.filter(category=category, available=True)
        .select_related("restaurant", "category")
    )

    paginator = Paginator(foods_list, 12)
    page = request.GET.get("page")

    try:
        foods = paginator.page(page)
    except PageNotAnInteger:
        foods = paginator.page(1)
    except EmptyPage:
        foods = paginator.page(paginator.num_pages)

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    return render(
        request,
        "menu/menu.html",
        {
            "foods": foods,
            "categories": Category.objects.all(),
            "selected_category": category,
            "cart_count": cart_count,
            "paginator": paginator,
        },
    )


def food_detail(request, pk):
    food = get_object_or_404(Food, id=pk, available=True)

    reviews = (
        Review.objects.filter(food=food)
        .select_related("user")
        .order_by("-created_at")
    )

    avg_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"] or 0

    user_review = None
    can_review = False

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        can_review = True

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    return render(
        request,
        "menu/food_detail.html",
        {
            "food": food,
            "reviews": reviews,
            "avg_rating": avg_rating,
            "user_review": user_review,
            "can_review": can_review,
            "cart_count": cart_count,
        },
    )