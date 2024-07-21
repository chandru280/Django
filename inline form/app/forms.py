from django import forms
from django.forms.models import inlineformset_factory
from .models import Testname, Testsubject

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



# # forms.py
# from django import forms
# from .models import Mark, Testname

# class MarkForm(forms.ModelForm):
#     class Meta:
#         model = Mark
#         fields = ['student', 'test', 'subject', 'marks']

#     def __init__(self, *args, **kwargs):
#         super(MarkForm, self).__init__(*args, **kwargs)
#         self.fields['subject'].queryset = Testname.objects.none()

#         if 'test' in self.data:
#             try:
#                 test_id = int(self.data.get('test'))
#                 self.fields['subject'].queryset = Testsubject.objects.filter(test_name_id=test_id)
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty subject queryset
#         elif self.instance.pk:
#             self.fields['subject'].queryset = self.instance.test.testsubject_set




 
from django import forms
from .models import Mark, Testname, Student

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