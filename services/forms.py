from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Makes the password input hidden.
        }


from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'payment_terms', 'service_price', 'service_package', 'service_tax', 'service_image']