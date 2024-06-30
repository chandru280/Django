# views.py

from django.shortcuts import render, redirect
from .models import Car, UserProfile, Book, Manufacturer
from .forms import AuthorForm, ManufacturerForm, UserForm, UserProfileForm, BookForm, CarForm


def index(request):
    return render(request, 'index.html')
 
def user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserForm()
    return render(request, 'user.html', {'form': form})

def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm()
    return render(request, 'user_profile.html', {'form': form})



def Authorform(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book')
    else:
        form = AuthorForm()
    return render(request, 'Author.html', {'form': form})


def book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book')
    else:
        form = BookForm()
    return render(request, 'book.html', {'form': form})


def Manufacturerform(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car')
    else:
        form = ManufacturerForm()
    return render(request, 'Manufacturer.html', {'form': form})

def car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car')
    else:
        form = CarForm()
    return render(request, 'car.html', {'form': form})



def user_profile_view(request):
    user_profiles = UserProfile.objects.all()  # Fetching all user profiles
    return render(request, 'userprofileView.html', {'user_profiles': user_profiles})


def book_view(request):
    books = Book.objects.all()
    return render(request, 'bookView.html', {'books': books})

def car_view(request):
    cars = Car.objects.all()
    return render(request, 'carView.html', {'cars': cars})