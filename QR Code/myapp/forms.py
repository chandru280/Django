from django import forms
from myapp.models import  *



class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = '__all__'