from django import forms
from .models import Answer

class TakeQuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                queryset=Answer.objects.filter(question=question),
                widget=forms.RadioSelect,
                label=question.text,
                empty_label=None,
            )
