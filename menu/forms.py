from django import forms
from .models import Food, Category


class FoodSearchForm(forms.Form):
    """Form for searching and filtering foods"""
    
    search_query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by food name...',
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('name', 'Name (A-Z)'),
            ('-name', 'Name (Z-A)'),
            ('price', 'Price (Low to High)'),
            ('-price', 'Price (High to Low)'),
            ('-created_at', 'Newest First'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
