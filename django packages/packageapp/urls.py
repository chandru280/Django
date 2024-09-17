from django.urls import path 
from packageapp import views  

urlpatterns = [
    path('people/', views.person_list_view, name='person-list'),
    path('update/<int:pk>/', views.update_person, name='update_person'),
    path('delete/<int:pk>/', views.delete_person, name='delete_person'),
]
