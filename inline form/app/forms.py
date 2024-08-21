from django import forms
from django.forms.models import inlineformset_factory
from .models import Testname, Testsubject,Mark, Student


class TestnameForm(forms.ModelForm):
    class Meta:
        model = Testname
        fields = ['test_name', 'standard']

TestsubjectFormSet = inlineformset_factory(
    Testname,
    Testsubject,
    fields=('subject',),
    extra=1,
    can_delete=True
)


class TestSelectionForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Select Student")
    test = forms.ModelChoiceField(queryset=Testname.objects.all(), label="Select Test")

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['marks']

    def __init__(self, *args, **kwargs):
        subject_name = kwargs.pop('subject_name', None)
        super(MarkForm, self).__init__(*args, **kwargs)
        if subject_name:
            self.fields['marks'].label = f'Enter marks for {subject_name}'




class MarkForm2(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['subject', 'marks']

MarkFormSet = inlineformset_factory(
    Testname, Mark, form=MarkForm,
    fields=['subject', 'marks'], extra=0, can_delete=False
)