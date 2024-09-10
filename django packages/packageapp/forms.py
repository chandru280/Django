# forms.py
from django import forms

class PersonSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search...'}))
