# models.py

from django.db import models
from django.contrib.auth.models import User


# One-to-One Relationship
class user(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
    
class UserProfile(models.Model):
    name = models.OneToOneField(user, on_delete=models.CASCADE)
    bio = models.TextField()
    location = models.CharField(max_length=100)
   
    def __str__(self):
        return f'{self.name}'


# Many-to-Many Relationship
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return f'{self.title}'


# Many-to-One Relationship
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.manufacturer}'
