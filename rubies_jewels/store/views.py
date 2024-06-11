from django.shortcuts import render, get_object_or_404
from .models import * 
from .forms import PhotoForm, CustomUserCreationForm, EmailAuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate


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
    return render(request, 'store/about.html')

def shop(request):
    return render(request, 'store/shop_categories.html', {"categories": Category.objects.all()})

def shop_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    # products = Product.objects.all()

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

def product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product.html', {'product': product})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            errors = form.errors.as_json()
    else:
        form = CustomUserCreationForm()
        errors = None
    
    return render(request, 'auth/signup.html', {'form': form, 'errors': errors})


def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                errors = form.errors.as_json()
        else:
            errors = form.errors.as_json()
    else:
        form = EmailAuthenticationForm()
        errors = None

    return render(request, 'auth/login.html', {'form': form, 'errors': errors})

def logout_view(request):
    logout(request)
    return redirect('/')