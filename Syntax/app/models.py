import uuid
from django.db import models
from django.utils.text import slugify

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    is_active = models.BooleanField(default=False)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    hobbies = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/')
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    slug = models.SlugField(unique=True)
    urlslug = models.CharField(max_length=100, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(MyModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
