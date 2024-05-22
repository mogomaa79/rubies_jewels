from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import Email


def index(request):
    return render(request, 'store/index.html')

def about(request):
    storage = get_messages(request)
    message = list(storage)[-1] if storage else None
    if message is None:
        return render(request, 'store/about.html')
    return render(request, 'store/about.html', {'message': message})

def shop(request):
    return render(request, 'store/shop.html')

def blog(request):
    return render(request, 'store/blog.html')

def handle_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Email not provided!')
            return HttpResponseRedirect('/about')
        
        Email.objects.create(email=email)
        messages.success(request, 'Email successfully submitted!')
        return HttpResponseRedirect('/about')
    
    messages.info(request, 'No POST request made.')
    return HttpResponseRedirect('/about')
