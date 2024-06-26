from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    mobile_number = forms.CharField(max_length=13)
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('mobile_number', 'address', 'password1', 'password2', 'role', 'username')
