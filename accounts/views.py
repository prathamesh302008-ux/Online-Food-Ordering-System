from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings

from .forms import (
    SignupForm, UserProfileForm, ChangePasswordForm,
    ForgotPasswordForm, ResetPasswordForm
)
from .models import UserProfile


def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            
            # Create UserProfile
            UserProfile.objects.create(user=user)
            
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}! Your account has been created.")
            return redirect("/")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            next_page = request.GET.get('next', '/')
            return redirect(next_page)
        else:
            messages.error(request, "Invalid Username or Password")
            return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")


@login_required(login_url='login')
def profile_view(request):
    """Display user profile"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    return render(request, "accounts/profile.html", {"profile": profile})


@login_required(login_url='login')
def edit_profile_view(request):
    """Edit user profile"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update user fields
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.last_name = form.cleaned_data.get('last_name', request.user.last_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()
            
            # Update profile
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required(login_url='login')
def change_password_view(request):
    """Change user password"""
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            
            if not user.check_password(old_password):
                messages.error(request, "Current password is incorrect.")
                return redirect('change_password')
            
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = ChangePasswordForm()

    return render(request, "accounts/change_password.html", {"form": form})


def forgot_password_view(request):
    """Request password reset"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
                
                # Generate token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Create reset link
                reset_link = f"{request.build_absolute_uri('/accounts/reset-password/')}{uid}/{token}/"
                
                # Send email
                subject = "Password Reset Request"
                message = f"""
                Hi {user.first_name},
                
                Please click the link below to reset your password:
                {reset_link}
                
                This link will expire in 24 hours.
                
                If you didn't request this, please ignore this email.
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, "Password reset link has been sent to your email.")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
            except Exception as e:
                messages.error(request, f"Error sending email: {str(e)}")
    else:
        form = ForgotPasswordForm()

    return render(request, "accounts/forgot_password.html", {"form": form})


def reset_password_view(request, uidb64, token):
    """Reset password with token"""
    if request.user.is_authenticated:
        return redirect('/')
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if not default_token_generator.check_token(user, token):
            messages.error(request, "Invalid or expired reset link.")
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid reset link.")
        return redirect('login')
    
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successfully! You can now login.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = ResetPasswordForm()

    return render(request, "accounts/reset_password.html", {"form": form, "uidb64": uidb64, "token": token})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("/")