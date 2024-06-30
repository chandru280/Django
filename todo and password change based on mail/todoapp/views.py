from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import todo
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, MyForm


def home(request):
    return render(request, 'home.html')

@login_required
def studentlist(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todo.html', context)

@login_required
def DeleteTask(request, pk):
    get_todo = todo.objects.get(user=request.user, pk = pk)
    get_todo.delete()
    return redirect('home')

@login_required
def change(request, pk):
    obj = todo.objects.get(pk=pk)
    if request.method == "POST":
        form = todo(request.method, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('index') 
        return redirect('update')
    else:
        form = todo
    
    context = {'form':form}
    return render(request,'todo.html',context)

@login_required
def Update(request, pk):
    get_todo = todo.objects.get(user=request.user, pk=pk)
    get_todo.status = True
    get_todo.save()
    return redirect('home')

@login_required
def Undo(request, pk):
    get_todo = todo.objects.get(user=request.user, pk=pk)
    get_todo.status = False
    get_todo.save()
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = MyForm(request.POST)  
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('studentlist')  
            else: 
                return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
    form = MyForm()
    return render(request, 'login.html', {'form': form})








@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


