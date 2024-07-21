"""
URL configuration for doctor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# appointment_system/urls.py
from django.contrib import admin
from appoinment import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
        # path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),

    path('add_working_hours/', views.add_working_hours, name='add_working_hours'),
    # path('available_timeslots/<int:doctor_id>/', views.available_timeslots, name='available_timeslots'),
     path('add-appointment/', views.add_appointment, name='add_appointment'),
    path('load-time-slots/', views.load_time_slots, name='load_time_slots'),
]
