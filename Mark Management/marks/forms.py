from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from marks.models import Mark, Staff, Standard, Student, Subject, Testname, Testsubject, UserForm  
from django.forms.models import inlineformset_factory




class Registrationform(UserCreationForm):
   
   
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-input w-full text-start border border-2 border-gray-200 outline-none px-8 py-3  rounded-md text-gray-800 text-sm  pt-3 focus:border-violet-400 focus:border-2 focus:outline-none transition ease-in-out duration-500   dark:focus:border-accent',}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-input w-full text-start border border-2 border-gray-200 outline-none px-8 py-3  rounded-md text-gray-800 text-sm  pt-3 focus:border-violet-400 focus:border-2 focus:outline-none transition ease-in-out duration-500  dark:focus:border-accent',}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-input w-full text-start border border-2 border-gray-200 outline-none px-8 py-3  rounded-md text-gray-800 text-sm  pt-3 focus:border-violet-400 focus:border-2 focus:outline-none transition ease-in-out duration-500  dark:focus:border-accent','data-toggle': 'password', 'id': 'password', }))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-input w-full text-start border border-2 border-gray-200 outline-none px-8 py-3  rounded-md text-gray-800 text-sm  pt-3 focus:border-violet-400 focus:border-2 focus:outline-none transition ease-in-out duration-500  dark:focus:border-accent','data-toggle': 'password', 'id': 'password', }))

    class Meta:
        model = UserForm
        fields = ['username', 'email', 'password1', 'password2', 'role']





class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = []


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__' 



class StandardForm(forms.ModelForm):
    class Meta:
        model = Standard
        fields = ['standard']

SubjectFormSet = inlineformset_factory(
        Standard,
        Subject,
        fields=('name',),
        extra=1,
        can_delete=True
    )



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




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = []


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__' 




class TestSelectionForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Select Student")
    test = forms.ModelChoiceField(queryset=Testname.objects.all(), label="Select Test")

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(TestSelectionForm, self).__init__(*args, **kwargs)
        if 'student' in initial:
            self.fields['student'].initial = initial['student']
        if 'test' in initial:
            self.fields['test'].initial = initial['test']

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['marks']

    def __init__(self, *args, **kwargs):
        subject_name = kwargs.pop('subject_name', None)
        super(MarkForm, self).__init__(*args, **kwargs)
        if subject_name:
            self.fields['marks'].label = f'Enter marks for {subject_name}'


