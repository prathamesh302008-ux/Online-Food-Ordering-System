from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:food_id>/", views.add_review, name="add_review"),
    path("delete/<int:review_id>/", views.delete_review, name="delete_review"),
    path("my-reviews/", views.my_reviews, name="my_reviews"),
]
