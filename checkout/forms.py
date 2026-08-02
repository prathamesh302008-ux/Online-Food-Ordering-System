from django import forms
from .models import DeliveryAddress, OrderCheckout


class DeliveryAddressForm(forms.ModelForm):

    class Meta:
        model = DeliveryAddress

        fields = [
            "full_name",
            "phone",
            "email",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "pincode",
            "country",
            "is_default",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Full Name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),

            "address_line1": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "House No / Street",
                }
            ),

            "address_line2": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Landmark (Optional)",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "City",
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "State",
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Pincode",
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Country",
                }
            ),

            "is_default": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class CheckoutForm(forms.ModelForm):

    delivery_address = forms.ModelChoiceField(
        queryset=DeliveryAddress.objects.none(),
        widget=forms.RadioSelect,
        required=True,
        empty_label=None,
    )

    payment_method = forms.ChoiceField(

        choices=[

            ("COD", "Cash On Delivery"),

            ("UPI", "UPI"),

            ("Google Pay", "Google Pay"),

            ("PhonePe", "PhonePe"),

            ("Paytm", "Paytm"),

            ("Credit Card", "Credit Card"),

            ("Debit Card", "Debit Card"),

            ("Net Banking", "Net Banking"),

        ],

        widget=forms.RadioSelect,

    )

    class Meta:

        model = OrderCheckout

        fields = [

            "coupon_code",

            "special_instructions",

        ]

        widgets = {

            "coupon_code": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Coupon Code",

                }

            ),

            "special_instructions": forms.Textarea(

                attrs={

                    "class": "form-control",

                    "rows": 3,

                    "placeholder": "Special Instructions",

                }

            ),

        }

    def __init__(self, *args, user=None, **kwargs):

        super().__init__(*args, **kwargs)

        if user:

            self.fields["delivery_address"].queryset = DeliveryAddress.objects.filter(

                user=user

            ).order_by(

                "-is_default",

                "-id",

            )


class QuickCheckoutForm(forms.Form):

    full_name = forms.CharField(

        max_length=150,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "Full Name",

            }

        ),

    )

    phone = forms.CharField(

        max_length=15,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "Phone Number",

            }

        ),

    )

    email = forms.EmailField(

        widget=forms.EmailInput(

            attrs={

                "class": "form-control",

                "placeholder": "Email",

            }

        ),

    )

    address = forms.CharField(

        widget=forms.Textarea(

            attrs={

                "class": "form-control",

                "rows": 3,

                "placeholder": "Complete Address",

            }

        ),

    )

    payment_method = forms.ChoiceField(

        choices=[

            ("COD", "Cash On Delivery"),

            ("UPI", "UPI"),

            ("Google Pay", "Google Pay"),

            ("PhonePe", "PhonePe"),

            ("Paytm", "Paytm"),

            ("Credit Card", "Credit Card"),

            ("Debit Card", "Debit Card"),

            ("Net Banking", "Net Banking"),

        ],

        widget=forms.RadioSelect,

    )

    coupon_code = forms.CharField(

        required=False,

        widget=forms.TextInput(

            attrs={

                "class": "form-control",

                "placeholder": "Coupon Code",

            }

        ),

    )