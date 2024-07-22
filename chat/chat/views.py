from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Message
from .forms import MessageForm

def chat(request):
    messages = Message.objects.all().order_by('created_on')
    form = MessageForm()
    return render(request, "chat.html", {'messages': messages, 'form': form})

@require_POST
def send_message(request):
    form = MessageForm(request.POST, request.FILES)
    if form.is_valid():
        message = form.save(commit=False)
        message.user = request.user
        message.save()
    return redirect('chat')
