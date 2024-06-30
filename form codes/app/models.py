
from django.db import models

choices = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
        ('5', 'Option 5'),
    ]



class MyModel(models.Model):
    text_field = models.CharField(max_length=100)
    integer_field = models.IntegerField()
    float_field = models.FloatField()
    boolean_field = models.BooleanField(default=False)
    date_field = models.DateField()
    time_field = models.TimeField()
    datetime_field = models.DateTimeField()
    email_field = models.EmailField()
    url_field = models.URLField()
    file_field = models.FileField(upload_to='uploads/', null=True, blank = True)
    image_field = models.ImageField(upload_to='images/', null=True, blank = True)
    choice_field = models.CharField(max_length=10, choices=[('1', 'Option 1'), ('2', 'Option 2')])
    multi_choice_field = models.CharField(max_length=10, choices=choices)
    char_field = models.CharField(max_length=50)
    decimal_field = models.DecimalField(max_digits=5, decimal_places=2)
    duration_field = models.DurationField(null=True, blank = True)
    slug_field = models.SlugField(null=True, blank = True)
    uuid_field = models.UUIDField(null=True, blank = True)
    ip_address_field = models.GenericIPAddressField(protocol='IPv4',null=True, blank = True)
    generic_ip_address_field = models.GenericIPAddressField(null=True, blank = True)
