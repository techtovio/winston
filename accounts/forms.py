from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
import re

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'id': 'password1'}),
        help_text="Password must contain at least 8 characters, including uppercase, lowercase, and numbers.",
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'id': 'password2'}),
        strip=False,
    )
    
    USER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('organization', 'Organization'),
        ('government', 'Government'),
    )
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='individual'
    )
    
    organization_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Organization name'}),
        label="Organization Name"
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'user_type', 'organization_name')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search('[A-Z]', password1):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search('[a-z]', password1):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search('[0-9]', password1):
            raise ValidationError("Password must contain at least one number.")
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        organization_name = cleaned_data.get('organization_name')
        
        if user_type in ['organization', 'government'] and not organization_name:
            self.add_error('organization_name', 'Organization name is required for this user type.')
        
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        strip=False,
    )