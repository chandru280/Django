from django.shortcuts import render
from django_tables2 import RequestConfig
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Person
from .tables import PersonTable

def person_list_view(request):
    query = request.GET.get('query', '')

    if query:
        persons = Person.objects.filter(name__icontains=query)
    else:
        persons = Person.objects.all()

    table = PersonTable(persons)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)

    # Handle AJAX request for live search
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('person_table.html', {'table': table, 'ajax': True}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'person_list.html', {'table': table})
