from django import forms
from .models import Cart


class AddToCartForm(forms.ModelForm):
    """Form for adding items to cart"""
    
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 1,
            })
        }


class CartUpdateForm(forms.ModelForm):
    """Form for updating cart items"""
    
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            })
        }
