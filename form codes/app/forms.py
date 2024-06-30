
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from .models import MyModel




choices = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
        ('5', 'Option 5'),
    ]
    

# class MyForm(forms.ModelForm):
#     class Meta:
#         model = MyModel
#         fields = '__all__'



#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['date_field'].widget = forms.DateInput(attrs={"type":"date"})
#         self.fields['datetime_field'].widget = forms.DateTimeInput(attrs={"type":"date"})
#         self.fields['time_field'].widget = forms.TimeInput(attrs={"type":"time"})
#         self.fields['multi_choice_field'].widget = forms.CheckboxSelectMultiple(choices=choices)

        




class MyForm(forms.Form):
    text_field = forms.CharField(max_length=100)
    integer_field = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    float_field = forms.FloatField()
    boolean_field = forms.BooleanField(required=False)
    date_field = forms.DateField(initial=timezone.now)
    time_field = forms.TimeField(initial=timezone.now)
    datetime_field = forms.DateTimeField(initial=timezone.now)
    email_field = forms.EmailField()
    url_field = forms.URLField()
    file_field = forms.FileField()
    image_field = forms.ImageField()
    choice_field = forms.ChoiceField(choices=[('1', 'Option 1'), ('2', 'Option 2')])
    multi_choice_field = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
    char_field = forms.CharField(max_length=50)
    decimal_field = forms.DecimalField(max_digits=5, decimal_places=2,required=False)
    duration_field = forms.DurationField(required=False)
    slug_field = forms.SlugField(required=False)
    uuid_field = forms.UUIDField(required=False)
    ip_address_field = forms.GenericIPAddressField(protocol='IPv4',required=False)
    generic_ip_address_field = forms.GenericIPAddressField(required=False)
