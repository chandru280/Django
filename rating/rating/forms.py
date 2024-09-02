from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'description']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} stars') for i in range(1, 6)]),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a review...'}),
        }
