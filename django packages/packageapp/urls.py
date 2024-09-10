from django.urls import path 
from packageapp import views  

urlpatterns = [
    path('people/', views.person_list_view, name='person-list'),
 
]
