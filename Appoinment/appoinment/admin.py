from django.contrib import admin
from .models import Doctor, Patient, DoctorWorkingHours, DoctorAppointment, TimeSlot

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(DoctorWorkingHours)
admin.site.register(DoctorAppointment)
admin.site.register(TimeSlot)
