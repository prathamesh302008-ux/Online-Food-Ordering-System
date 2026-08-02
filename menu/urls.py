from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.menu,
        name="menu"
    ),

    path(
        "category/<int:category_id>/",
        views.category_foods,
        name="category_foods"
    ),

    path(
        "food/<int:pk>/",
        views.food_detail,
        name="food_detail"
    ),

]