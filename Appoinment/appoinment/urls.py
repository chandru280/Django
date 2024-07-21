# appointments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('add_working_hours/', views.add_working_hours, name='add_working_hours'),
    path('available_timeslots/<int:doctor_id>/', views.available_timeslots, name='available_timeslots'),
]
