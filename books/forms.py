from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class GuestPurchaseForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already registered. Please login to purchase."
            )
        return email

class AccountPurchaseForm(forms.Form):
    # Could include payment method selection, etc.
    pass