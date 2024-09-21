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
    fields=('subject', 'total_mark', 'pass_mark'),
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
        student = kwargs.pop('student', None)
        super(TestSelectionForm, self).__init__(*args, **kwargs)
        if student:
            self.fields['student'].initial = student

        # Exclude already saved tests for the selected student
        if student:
            saved_tests = Mark.objects.filter(student=student).values_list('test', flat=True)
            self.fields['test'].queryset = Testname.objects.exclude(id__in=saved_tests)






class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['marks']

    def __init__(self, *args, **kwargs):
        subject = kwargs.pop('subject', None)
        super(MarkForm, self).__init__(*args, **kwargs)
        if subject:
            self.fields['marks'].label = f'Enter marks for {subject.subject}'

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        total_mark = self.initial.get('total_mark')
        pass_mark = self.initial.get('pass_mark')
    
        print(f'Marks: {marks}, Total Mark: {total_mark}, Pass Mark: {pass_mark}')  # Debugging
    
        if marks is not None and total_mark is not None:
            if marks > total_mark:
                raise forms.ValidationError(f'Enter a valid mark, it cannot be greater than the total mark {total_mark}.')
        
        if marks is not None and pass_mark is not None:
            status = 'Pass' if marks >= pass_mark else 'Fail'
            self.initial['status'] = status   
    
        return marks
    
    
    
    
    
    


class MarkFormupdate(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['marks']  
    def __init__(self, *args, **kwargs):
        self.total_mark = kwargs.pop('total_mark', None)
        self.pass_mark = kwargs.pop('pass_mark', None)
        super(MarkFormupdate, self).__init__(*args, **kwargs)

    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        total_mark = self.total_mark   
        pass_mark = self.pass_mark     

        
        if marks is not None and total_mark is not None:
            if marks > total_mark:
                raise forms.ValidationError(f'Enter a valid mark, it cannot be greater than the total mark {total_mark}.')
        
        if marks is not None and pass_mark is not None:
            status = 'Pass' if marks >= pass_mark else 'Fail'
            self.initial['status'] = status 
    
        return marks
