
from django import forms
from .models import CoffeeBeanBatch
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddBatchForm(forms.ModelForm):
    class Meta:
        model = CoffeeBeanBatch
        fields = ['batch_id', 'farm_name', 'origin_country', 'harvest_date', 'processing_details', 'roasting_date', 'packaging_details', 'packaging_date', 'is_shipped', 'is_delivered', 'current_location']
        # Use widgets if you need to customize the form fields

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
