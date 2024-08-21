from django import forms
from .models import  Quiz, Question
from django.forms.models import inlineformset_factory


class TakeQuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        for question in questions:
            choices = [
                (question.option1, question.option1),
                (question.option2, question.option2),
                (question.option3, question.option3),
            ]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.question,
                required=True,
            )

class QuiznameForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

