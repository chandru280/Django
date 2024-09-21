from django.urls import path 
from marks import views
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('login/', views.user_login, name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), # Redirect to the current url after will login using auth function

    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),



    path('standard_list/', views.standard_list, name='standard_list'),
    path('subject_list/<int:standard_id>/', views.subject_list, name='subject_list'),
  
  
  
  
    path('create_testname/', views.create_testname_with_subjects, name='create_testname_with_subjects'),
    path('fetch_subjects/', views.fetch_subjects, name='fetch_subjects'),

    path('students/', views.student_list, name='student_list'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student_add/', views.add_student, name='add_student'),
    path('student/<int:student_id>/update/', views.update_student, name='update_student'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
   

    path('list_staff/', views.staff_list, name='staff_list'),
    path('add_staff/', views.staff_add, name='staff_add'),
    path('<int:staff_id>/update/', views.staff_update, name='staff_update'),
    path('<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),



    path('create_marks/<int:student_id>/', views.create_marks, name='create_marks'),
    path('ajax/get-subjects/', views.get_subjects, name='get_subjects'),
    path('update_mark/<int:mark_id>/', views.update_mark, name='update_mark'),

    path('manage-permissions/', views.manage_user_permissions, name='manage_user_permissions'),
   

     path('student/<int:pk>/', views.student_detail, name='student_detail'),


 path('standard/create/', views.add_or_update_standard, name='create_standard'),
    path('standard/update/<int:standard_id>/', views.add_or_update_standard, name='update_standard'),
    path('standard/delete/<int:standard_id>/', views.delete_standard, name='delete_standard'),
    path('subject/delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),

     
    ]
