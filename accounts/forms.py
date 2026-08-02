from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        fields = ['mobile', 'profile_image', 'date_of_birth']
        widgets = {
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class ChangePasswordForm(forms.Form):
    """Form for changing password"""
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Current Password'
        })
    )
    
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password != confirm_password:
            raise forms.ValidationError("New passwords do not match.")
        
        return cleaned_data


class ForgotPasswordForm(forms.Form):
    """Form for password reset"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )


class ResetPasswordForm(forms.Form):
    """Form for resetting password with token"""
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password'
        })
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data