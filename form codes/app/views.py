from django.shortcuts import render, redirect
from .forms import MyForm
from .models import MyModel

def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my-view')
    else:
        form = MyForm()
    return render(request, 'my_template.html', {'form': form})
