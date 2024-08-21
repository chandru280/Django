from django.urls import path
from . import views


urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('addquiz/', views.create_quiz, name='addquiz'),
    path('update/<int:quiz_id>/', views.update_quiz, name='update_quiz'),
    

    path('addquestion/', views.create_question, name='addquestion'),
    path('update_question/<int:question_id>/', views.update_question, name='update_question'),
  

    
]
