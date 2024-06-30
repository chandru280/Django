# forms.py
 
from django import forms
from .models import Manufacturer, UserProfile, Book, Car, user, Author


class UserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'location']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        existing_users = UserProfile.objects.values_list('name__id', flat=True)
        self.fields['name'].queryset = user.objects.exclude(id__in=existing_users)



class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors']


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['manufacturer', 'model']
