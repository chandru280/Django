from django.urls import path 
from marks import views


urlpatterns = [

    path('add_standard_subject_form',views.add_standart_with_subject, name = 'add_standard_subject_form'),

    path('standard_list/', views.standard_list, name='standard_list'),
    path('subject_list/<int:standard_id>/', views.subject_list, name='subject_list'),
  
  
  
  
    path('create_testname/', views.create_testname_with_subjects, name='create_testname_with_subjects'),


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

    ]