from django.shortcuts import render, redirect, get_object_or_404
from .models import Staff, Student, Event, Notification
from .forms import StaffForm, StudentForm, EventForm
from django.contrib.auth.decorators import login_required

# Staff CRUD
@login_required
def create_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'staff_form.html', {'form': form})

@login_required
def update_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'staff_form.html', {'form': form})

@login_required
def delete_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff_list')
    return render(request, 'confirm_delete.html', {'object': staff})

@login_required
def list_staff(request):
    staffs = Staff.objects.all()
    return render(request, 'staff_list.html', {'staffs': staffs})

# Student CRUD
@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'confirm_delete.html', {'object': student})

@login_required
def list_student(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# Event creation and notification
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user.staff
            event.save()
            students = Student.objects.all()
            for student in students:
                Notification.objects.create(event=event, student=student)
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@login_required
def list_event(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})







from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or another page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Redirect to home or another page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')  # Redirect to login page or home page after logout

def home(request):
    return render(request, 'home.html')
