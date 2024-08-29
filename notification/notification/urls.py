"""notification URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from message import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

 path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
   
    path('register/', views.register, name='register'),

    path('staff/create/', views.create_staff, name='create_staff'),
    path('staff/<int:pk>/update/', views.update_staff, name='update_staff'),
    path('staff/<int:pk>/delete/', views.delete_staff, name='delete_staff'),
    path('staff/', views.list_staff, name='staff_list'),
    path('student/create/', views.create_student, name='create_student'),
    path('student/<int:pk>/update/', views.update_student, name='update_student'),
    path('student/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('student/', views.list_student, name='student_list'),
    path('event/create/', views.create_event, name='create_event'),
    path('events/', views.list_event, name='event_list'),
    # path('notifications/', views.notification_list, name='notification_list'),
]
