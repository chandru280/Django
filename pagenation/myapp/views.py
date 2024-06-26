from django.shortcuts import render, redirect
from django.views import View
from .models import Item
from .forms import RandomNameForm
import random
import string
from django.views.generic import ListView
from django.core.paginator import Paginator

class GenerateRandomNamesView(View):
    template_name = 'generate_random_names.html'

    def get(self, request):
        form = RandomNameForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RandomNameForm(request.POST)
        if form.is_valid():
            number_of_names = form.cleaned_data['number_of_names']
            for _ in range(number_of_names):
                random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                # random.choices is used to select 10 random characters from the combined pool of ASCII letters and digits.
                Item.objects.create(name=random_name)
            return redirect('item_list')  
        return render(request, self.template_name, {'form': form})




def item_list(request):
 item_list = Item.objects.all()

 paginator = Paginator(item_list, 10) 
    #The Paginator class from django.core.paginator is used to handle pagination.
    # paginator is initialized with item_list and the number 10, meaning each page will display 10 items.

 page_number = request.GET.get('page')

    #This line retrieves the current page number from the request’s GET parameters.
    # request.GET.get('page') looks for a parameter named page in the URL query string. For example, if the URL is ...?page=2, page_number will be '2'.
    # If no page parameter is found, page_number will be None.

 page_obj = paginator.get_page(page_number)
 
    #The get_page method of the Paginator class returns a Page object.
    #If page_number is None or invalid, get_page returns the first page.
    #The Page object (page_obj) contains the items for the current page and additional pagination information.
    
 return render(request, 'item_list.html', {'page_obj': page_obj})






import pandas as pd
from django.http import HttpResponse
from .models import Item

def export_items_to_excel(request):
 
    items = Item.objects.all()
    data = []
    for item in items:
        data.append({
        'Name': item.name,
        })
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="items.xlsx"'
    df.to_excel(response, index=False)
    return response



#another metho to downlod excel

# def export_items_to_excel(request):
#     items = Item.objects.all()
#     data = []
#     for item in items:
#         data.append({
#         'Name': item.name,
#         })
#     df = pd.DataFrame(data)
#     with pd.ExcelWriter('items.xlsx') as writer:
#         df.to_excel(writer, sheet_name='Items', index=False)
#         df.to_excel(writer, sheet_name='Backup', index=False)

#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="items.xlsx"'
#     # writer.save()
#     response.write(open('items.xlsx', 'rb').read())
#     return response