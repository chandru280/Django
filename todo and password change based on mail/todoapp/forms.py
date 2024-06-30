from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserForm
from captcha.fields import CaptchaField

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
   
    class Meta:
        model = UserForm
        fields = {
            'last_name',  
            'email',
            'first_name',
            'username',
           }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.username=self.cleaned_data['username']
        user.first_name=self.cleaned_data['first_name']
        user.last_name=self.cleaned_data['last_name']
        user.email=self.cleaned_data['email']
    

        if commit:
            user.save()
        return user 
    




class MyForm(forms.Form):
    captcha=CaptchaField()
