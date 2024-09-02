from django.shortcuts import render, redirect
from django.utils import translation

def home(request):
    context = {
        'welcome_message': ("Welcome to our website!"),
        'description': ("This is a multi-language site."),
    }
    return render(request, 'home.html', context)

def change_language(request, lang_code):
    print(f"Activating language: {lang_code}")  # Debug print
    translation.activate(lang_code)
    request.session[translation.LANGUAGE_SESSION_KEY] = lang_code
    return redirect('home')
