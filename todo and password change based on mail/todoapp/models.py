from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class todo(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length = 50)
    status = models.BooleanField(default = False)

    def __str__(self):
        return self.todo_name


class UserForm(User):
    email = models.EmailField(primary_key=True,unique=True),
    ID = models.CharField(max_length=3, primary_key=True)