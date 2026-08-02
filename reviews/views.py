from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from menu.models import Food
from .models import Review
from .forms import ReviewForm


@login_required(login_url="login")
def add_review(request, food_id):
    """Add or Update Review"""

    food = get_object_or_404(
        Food,
        id=food_id
    )

    existing_review = Review.objects.filter(
        user=request.user,
        food=food
    ).first()

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            if existing_review:

                existing_review.rating = form.cleaned_data["rating"]
                existing_review.review = form.cleaned_data["review"]
                existing_review.save()

                messages.success(
                    request,
                    "Review updated successfully!"
                )

            else:

                review = form.save(commit=False)

                review.user = request.user
                review.food = food

                review.save()

                messages.success(
                    request,
                    "Thank you for your review!"
                )

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":

                return JsonResponse({
                    "success": True,
                    "message": "Review saved successfully!"
                })

            return redirect(
                "food_detail",
                pk=food.id
            )

        else:

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":

                return JsonResponse({
                    "success": False,
                    "errors": form.errors
                }, status=400)

    else:

        if existing_review:
            form = ReviewForm(instance=existing_review)
        else:
            form = ReviewForm()

    context = {
        "form": form,
        "food": food,
        "existing_review": existing_review,
    }

    return render(
        request,
        "reviews/add_review.html",
        context,
    )


@login_required(login_url="login")
def delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user,
    )

    food_id = review.food.id

    review.delete()

    messages.success(
        request,
        "Review deleted successfully!"
    )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        return JsonResponse({
            "success": True,
            "message": "Review deleted successfully!"
        })

    return redirect(
        "food_detail",
        pk=food_id,
    )


@login_required(login_url="login")
def my_reviews(request):

    reviews = Review.objects.filter(
        user=request.user
    ).select_related(
        "food"
    ).order_by(
        "-created_at"
    )

    context = {
        "reviews": reviews,
    }

    return render(
        request,
        "reviews/my_reviews.html",
        context,
    )