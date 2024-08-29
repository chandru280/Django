from django.urls import path
from . import views

urlpatterns = [
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/update/<int:pk>/', views.staff_update, name='staff_update'),
    path('staff/delete/<int:pk>/', views.staff_delete, name='staff_delete'),
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/update/<int:pk>/', views.student_update, name='student_update'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('notifications/', views.notification_list, name='notification_list'),
]
