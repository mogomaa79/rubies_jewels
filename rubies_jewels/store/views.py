from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import * 
from .forms import PhotoForm
from django.core.paginator import Paginator

def upload(request):
  context = dict(backend_form=PhotoForm())

  if request.method == 'POST':
    form = PhotoForm(request.POST, request.FILES)
    context['posted'] = form.instance
    if form.is_valid():
        form.save()

  return render(request, 'store/upload.html', context)

def index(request):
    """Return main index with latest 3 products"""
    products = Product.objects.all().order_by('-id')[:4]
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
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': page_obj,
        'sort_by': sort_by,
    }
    return render(request, 'store/shop.html', context)

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
