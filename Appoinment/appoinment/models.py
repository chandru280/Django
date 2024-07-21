from datetime import datetime, timedelta
from django.db import models
# from django_appointment.models import WorkingHours, Appointment
from django.core.exceptions import ValidationError


class Doctor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DoctorWorkingHours(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_duration = models.PositiveIntegerField(help_text="Duration of each appointment in minutes")


    def __str__(self):
        return f"{self.doctor.name} - {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}"


class DoctorWorkingHours(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField(null=True, blank=True)
    appointment_duration = models.IntegerField()  # in minutes

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_time_slots()

    def create_time_slots(self):
        start_time = datetime.combine(self.date, self.start_time)
        end_time = datetime.combine(self.date, self.end_time)
        duration = timedelta(minutes=self.appointment_duration)

        while start_time + duration <= end_time:
            TimeSlot.objects.create(
                doctor=self.doctor,
                start_time=start_time,
                end_time=start_time + duration,
                date=self.date
            )
            start_time += duration

class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('doctor', 'start_time', 'end_time')

class DoctorAppointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_contact = models.CharField(max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField(null=True,blank=True)

    def save(self, *args, **kwargs):
        overlapping_appointments = DoctorAppointment.objects.filter(
            doctor=self.doctor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)

        if overlapping_appointments.exists():
            raise ValidationError("This time slot is already booked.")

        super().save(*args, **kwargs)



