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
