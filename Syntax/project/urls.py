# urls.py
from django.urls import path
from app import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_form_view, name='my_form'),
    path('success/', views.success_view, name='success'),
    path('my_model_data_view/', views.my_model_data_view, name='my_model_data_view'),

]
