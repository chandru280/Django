from django.contrib import admin
from .models import UserProfile, Author, Book, Manufacturer, Car
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Manufacturer)
admin.site.register(Car)
