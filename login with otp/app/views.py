from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OTP
import random
from django.core.mail import send_mail
from django.conf import settings


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.get_user()
            login(request, user)

            # Check if user has an email address
            if user.email:
                # Generate OTP
                otp_code = ''.join(random.choice('0123456789') for _ in range(6))
                OTP.objects.create(user=user, otp=otp_code)

                # Send OTP via email
                subject = 'Your OTP for Verification'
                message = f'Your OTP is: {otp_code}'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

                return redirect('enter_otp')
            else:
                messages.error(request, 'Please update your email address to receive OTPs.')
                return redirect('login')  # Redirect to a view for updating email
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def enter_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        user = request.user
        otp_obj = OTP.objects.filter(user=user, otp=otp_entered, is_verified=False).first()
        if otp_obj:
            otp_obj.is_verified = True
            otp_obj.save()
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP, please try again.')
    return render(request, 'enter_otp.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
