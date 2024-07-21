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


    path('create-testname/', views.create_testname_with_subjects, name='create_testname_with_subjects'),

# path('create-mark/', views.create_mark, name='create_mark'),
#     path('ajax/load-subjects/', views.load_subjects, name='load_subjects'),


    path('create-marks/', views.create_marks, name='create_marks'),
    path('ajax/get-subjects/', views.get_subjects, name='get_subjects'),

  path('manage_marks/<int:test_id>/', views.manage_marks, name='manage_marks'),
 






]
