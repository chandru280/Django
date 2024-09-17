# forms.py
from django import forms

from packageapp.models import Person

class PersonSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search...'}))

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'