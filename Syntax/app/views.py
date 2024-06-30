from django.shortcuts import render, redirect

from app.models import MyModel
from .forms import MyForm

def my_form_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')  
    else:
        form = MyForm()
    return render(request, 'my_form.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')



def my_model_data_view(request):
    my_model_instances = MyModel.objects.all()
    return render(request, 'my_model_data.html', {'my_model_instances': my_model_instances})