"""
URL configuration for project project.

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
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('user/', views.user, name="user"),
    path('userprofile/', views.user_profile, name='user_profile'),
    path('user-profile-view/', views.user_profile_view, name='user_profile_view'),


    path('Authorform/', views.Authorform, name='Authorform'),
    path('book/', views.book, name='book'),
    path('books-view/', views.book_view, name='books_view'),

    path('Manufacturerform/', views.Manufacturerform, name='Manufacturerform'),
    path('car/', views.car, name='car'),
    path('cars-view/', views.car_view, name='cars_view'),
]
