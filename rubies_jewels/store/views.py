from django.shortcuts import render, get_object_or_404
from .models import * 
from .forms import *
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


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
    return render(request, 'store/index.html', {'products': products, "categories": Category.objects.all()})

def about(request):
    return render(request, 'store/about.html')

def shop(request):
    return render(request, 'store/shop_categories.html', {"categories": Category.objects.all()})

def shop_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, stock__gt=0)
    # products = Product.objects.all()

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    # Pagination
    paginator = Paginator(products, 4)  # Show 4 products per page
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
            return redirect('shop')
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
                return redirect('shop')
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
    return redirect('shop')

@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == 'POST' and len(cart_items) > 0:
        # Create the order object
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price_after_discount,
            coupon=cart.coupon
        )
        
        # Add cart items to the order
        order_items = []
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )
            order_items.append(order_item)
            
            # Update product quantity (if needed)
            product.stock -= quantity
            product.save()
        
        # Clear the cart items after creating the order
        cart.items.all().delete()
        cart.coupon = None
        cart.save()

        return redirect('shop')
    
    return render(request, 'store/cart.html', {'cart': cart, 'cart_items': cart_items})

@login_required
def product_actions(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')

    if action == 'add_to_cart':
        # Add product to cart logic
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect('shop')  # Redirect to cart page

    elif action == 'buy_now':
        # Buy now logic
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        return redirect('checkout')  # Redirect to checkout page

    elif action == 'add_to_wishlist':
        # Add product to wishlist logic
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.items.add(product)
    
    elif action == 'remove_from_wishlist':
        # Remove product from wishlist logic
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        wishlist.items.remove(product)

    return redirect('product', product_id=product_id)

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'user': request.user,
    }
    return render(request, 'store/cart.html', context)

@login_required
def update_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if product.stock > cart_item.quantity:
            cart_item.quantity += 1
            cart_item.save()
        else:
            return render(request, 'store/cart.html', {
                'cart': cart,
                'user': request.user,
                'error': "Not enough left in stock"
            })
        
    elif action == 'decrease':
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.quantity -= 1
        if cart_item.quantity == 0:
            cart_item.delete()
        else:
            cart_item.save()

    return redirect('cart')

@login_required
@csrf_exempt
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            if Order.objects.filter(user=request.user, coupon=coupon).exists(): # check if there is an order which has this user and the coupon
                return render(request, 'store/cart.html', context={
                "user": request.user,
                "cart": cart,
                "error": "You already used this Coupon!"
            })
            else:
                cart.coupon = coupon
                cart.save()

        except Coupon.DoesNotExist:
            return render(request, 'store/cart.html', context={
                "user": request.user,
                "cart": cart,
                "error": "Invalid Coupon Code"
            })

    return redirect('cart')

@login_required
@csrf_exempt
def remove_coupon(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.coupon = None
    cart.save()
    return redirect('cart')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'auth/profile.html', {'form': form})