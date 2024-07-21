from datetime import datetime, timezone
from django import forms
from .models import Doctor, DoctorAppointment, DoctorWorkingHours


# class DoctorAppointmentForm(forms.ModelForm):
#     class Meta:
#         model = DoctorAppointment
#         fields = ['doctor', 'patient_name', 'patient_contact', 'start_time', 'end_time']

class DoctorWorkingHoursForm(forms.ModelForm):
    class Meta:
        model = DoctorWorkingHours
        fields = '__all__'


from django import forms
from .models import DoctorAppointment
# from .utils import calculate_available_timeslots  # Assuming the utility function is in utils.py





from django import forms
from .models import DoctorAppointment, TimeSlot

class DoctorAppointmentForm(forms.ModelForm):
    available_time_slots = forms.ModelChoiceField(
        queryset=TimeSlot.objects.none(),
        required=True,
        empty_label="Select a time slot"
    )

    class Meta:
        model = DoctorAppointment
        fields = ['doctor', 'patient_name', 'patient_contact', 'available_time_slots', 'date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'doctor' in self.data and 'date' in self.data:
            try:
                doctor_id = int(self.data.get('doctor'))
                date = self.data.get('date')
                self.fields['available_time_slots'].queryset = TimeSlot.objects.filter(
                    doctor_id=doctor_id, date=date, is_booked=False
                )
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['available_time_slots'].queryset = TimeSlot.objects.filter(
                doctor=self.instance.doctor,
                date=self.instance.start_time.date(),
                is_booked=False
            )
