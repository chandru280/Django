# forms.py
from django import forms
from .models import MyModel

class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = '__all__'
        
    widgets =  {


        'birth_date' : forms.DateInput(attrs={'type':'date'}),
    }