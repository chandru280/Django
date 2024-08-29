from django import forms
from .models import Staff, Student, Event

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['user', 'name']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'name']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description']



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')
