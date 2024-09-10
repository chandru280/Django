# views.py
from django_tables2 import RequestConfig
from django.shortcuts import render
from .models import Person
from .tables import PersonTable

def person_list_view(request):
    # Fetch data from the model (you can add filters here if needed)
    persons = Person.objects.all()
    
    # Create a table object and pass in the data
    table = PersonTable(persons)
    
    # RequestConfig helps with pagination and sorting
    RequestConfig(request, paginate={"per_page": 10}).configure(table)
    
    # Render the table in the template
    return render(request, 'personal_list.html', {'table': table})


