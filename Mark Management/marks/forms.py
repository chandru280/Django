from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from marks.models import Mark, Staff, Standard, Student, Subject, Testname, Testsubject, UserForm, AcademicYear  
from django.forms.models import inlineformset_factory




class Registrationform(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'id': 'password',
        })
    )
    password2 = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
            'id': 'password',
        })
    )
    
    class Meta:
        model = UserForm
        fields = ['username', 'email', 'password1', 'password2', 'role']

        widgets = {
            'role': forms.Select(attrs={
            'class': 'form-control',
        }) }



class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        exclude = []






class StandardForm(forms.ModelForm):
    class Meta:
        model = Standard
        fields = ['standard']
        widgets = {
            'standard': forms.TextInput(
                attrs={
                    'class': 'form-control',   
                    'placeholder': 'Enter Standard',   
                }
            )
        }

SubjectFormSet = inlineformset_factory(
    Standard,
    Subject,
    fields=('name',),
    extra=1,
    can_delete=True,
    widgets={
        'name': forms.TextInput(
            attrs={
                'class': 'form-control',  
                'placeholder': 'Enter Subject Name',  
            }
        )
    }
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
        exclude = ['academic_year',]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name'}),
            'standard': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Address'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Contact Number'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Guardian Name'}),
            'guardian_contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Guardian Contact'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'admission_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Admission Number'}),
            'nationality': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nationality'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'admission_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'previous_school': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Previous School'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Roll Number'}),
            'father_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Father\'s Name'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Father\'s Occupation'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Mother\'s Name'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Mother\'s Occupation'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {
                'required': 'This field is required.',
                'invalid': 'Enter a valid value.',
            }



class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__' 

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter Email'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Contact Number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Enter Address', 'rows': 4}),
            'designation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Designation'}),
            'department': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Department'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Enter Salary'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Nationality'}),
            'religion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Religion'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'qualification': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Qualification'}),
            'experience': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Experience'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }




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
