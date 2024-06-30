from django.contrib import admin
from django.urls import include, path 
from todoapp import views
from django.contrib.auth import views as auth_views 


urlpatterns = [
    path('',views.home, name = 'home'),
    path('studentlist', views.studentlist, name='studentlist'),
    
    path('delete-task/<int:pk>/', views.DeleteTask, name='delete'),
    path('update/<int:pk>/', views.Update, name='update'),
    path('undo/<int:pk>/', views.Undo, name='undo'),

    path('change/', views.change, name='change'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    

    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),







]
