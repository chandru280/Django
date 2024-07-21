from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Doctor, Patient, DoctorWorkingHours, DoctorAppointment
from .forms import DoctorAppointmentForm, DoctorWorkingHoursForm


# def book_appointment(request):
#     if request.method == 'POST':
#         form = DoctorAppointmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('appointment_success')
#     else:
#         form = DoctorAppointmentForm()
#     return render(request, 'book_appointment.html', {'form': form})


def add_working_hours(request):
    if request.method == 'POST':
        form = DoctorWorkingHoursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('working_hours_success')
    else:
        form = DoctorWorkingHoursForm()
    return render(request, 'add_working_hours.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Doctor, DoctorWorkingHours, DoctorAppointment
from .forms import DoctorAppointmentForm
from datetime import datetime, timedelta



# def available_timeslots(request, doctor_id):
#     doctor = get_object_or_404(Doctor, pk=doctor_id)
#     working_hours = DoctorWorkingHours.objects.filter(doctor=doctor)
#     appointments = DoctorAppointment.objects.filter(doctor=doctor)

#     # Calculate available timeslots
#     available_timeslots = calculate_available_timeslots(working_hours, appointments)

#     return render(request, 'available_timeslots.html', {'timeslots': available_timeslots})






from django.utils import timezone
from datetime import datetime, timedelta

def make_aware_if_naive(dt):
    if timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt

def calculate_available_timeslots(working_hours, appointments):
    available_slots = []

    # Ensure all appointments are timezone-aware
    appointments = [(make_aware_if_naive(app.start_time), make_aware_if_naive(app.end_time)) for app in appointments]
    
    for wh in working_hours:
        start = make_aware_if_naive(datetime.combine(datetime.today(), wh.start_time))
        end = make_aware_if_naive(datetime.combine(datetime.today(), wh.end_time))
        appointment_duration = timedelta(minutes=wh.appointment_duration)

        # Check each slot in the working hours for availability
        while start + appointment_duration <= end:
            slot_end = start + appointment_duration
            if not any(app_start < slot_end and app_end > start for app_start, app_end in appointments):
                available_slots.append((start.time(), slot_end.time()))
            start = slot_end

    return available_slots









from django.shortcuts import render, redirect
from .forms import DoctorAppointmentForm

def add_appointment(request):
    if request.method == 'POST':
        form = DoctorAppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            time_slot = form.cleaned_data['available_time_slots']
            appointment.start_time = time_slot.start_time
            appointment.end_time = time_slot.end_time
            appointment.save()

            # Mark the selected time slot as booked
            time_slot.is_booked = True
            time_slot.save()

            return redirect('appointment_success')
    else:
        form = DoctorAppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})



from django.http import JsonResponse
from .models import TimeSlot

def load_time_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    if doctor_id and date:
        time_slots = TimeSlot.objects.filter(
            doctor_id=doctor_id, date=date, is_booked=False
        ).values('id', 'start_time', 'end_time')
        print('1',time_slots)
        return JsonResponse(list(time_slots), safe=False)
    return JsonResponse([], safe=False)
