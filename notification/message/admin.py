from django.contrib import admin

# Register your models here.


from django.contrib import admin
from . models import (Staff, Student, 
                      Event,
                      Notification,CustomUser
                      )
                  
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(CustomUser)
