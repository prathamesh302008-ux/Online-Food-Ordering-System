from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("profile/", views.profile_view, name="profile"),
    path("edit-profile/", views.edit_profile_view, name="edit_profile"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/", views.reset_password_view, name="reset_password"),
    path("logout/", views.logout_view, name="logout"),
]