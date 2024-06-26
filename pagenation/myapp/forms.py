from django import forms

class RandomNameForm(forms.Form):
    number_of_names = forms.IntegerField(min_value=1, label="Number of Random Names")
