from django.shortcuts import render
from django_tables2 import RequestConfig
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Person
from .tables import PersonTable
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import PersonForm




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


def update_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm(instance=person)
    
    return render(request, 'update_person.html', {'form': form})

def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    
    return HttpResponse(status=405)