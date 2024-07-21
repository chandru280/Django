from django.contrib import admin
from .models import Student, Testname, Testsubject, Mark
# Register your models here.

admin.site.register(Student)
admin.site.register(Testname)
admin.site.register(Testsubject)
admin.site.register(Mark)