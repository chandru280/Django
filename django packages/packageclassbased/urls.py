from django.urls import path 
from packageclassbased import views  

urlpatterns = [
    path('people/', views.PersonListView.as_view(), name='person-list-class'),
 
]
