from django.contrib import admin
from .models import UserForm, Standard, Subject, Student, Staff, Testsubject, Testname, Mark


admin.site.register(UserForm)
admin.site.register(Standard)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Testname)
admin.site.register(Testsubject)
admin.site.register(Mark)
