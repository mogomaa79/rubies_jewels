from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import *
from django import forms
from django.http import HttpResponse
from cloudinary.forms import cl_init_js_callbacks      
from .forms import PhotoForm

def upload(request):
  context = dict( backend_form = PhotoForm())

  if request.method == 'POST':
    form = PhotoForm(request.POST, request.FILES)
    context['posted'] = form.instance
    if form.is_valid():
        form.save()

  return render(request, 'store/upload.html', context)

def index(request):
    """Return main index with latest 3 products"""
    products = Product.objects.all().order_by('-id')[:3]
    return render(request, 'store/index.html', {'products': products})

def about(request):
    storage = get_messages(request)
    message = list(storage)[-1] if storage else None
    if message is None:
        return render(request, 'store/about.html')
    return render(request, 'store/about.html', {'message': message})

def shop(request):
    return render(request, 'store/shop_categories.html', {"categories": Category.objects.all()})

def shop_category(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'store/shop.html', {'products': products, 'category': category})

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

def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product.html', {'product': product})
