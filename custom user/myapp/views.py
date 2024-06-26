from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages



def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        user = authenticate(request, username=mobile_number, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'ADMIN':
                return redirect('admin')
            elif user.role == 'STAFF':
                return redirect('staff')
            elif user.role == 'STUDENT':
                return redirect('student')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def admins(request):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    return render(request, 'admin.html')

@login_required
def staff(request):
    if not request.user.is_superuser and request.user.role != 'STAFF':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    return render(request, 'staff.html')

@login_required
def student(request):
    if not request.user.is_superuser and request.user.role != 'STUDENT':
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    return render(request, 'student.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})
