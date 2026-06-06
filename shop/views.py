import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Category, Product, Wishlist 
from cart.forms import CartAddProductForm
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm

# --- MAIN SHOP VIEWS ---

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    # Base WhatsApp URL for individual product inquiries
    msg = f"Hello! I am interested in this product from your store:\n\n* {product.name} *\nPrice: ₹{product.price}\nLink: {request.build_absolute_uri()}"
    encoded_msg = urllib.parse.quote(msg)
    whatsapp_url = f"https://wa.me/918983341944?text={encoded_msg}"

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'whatsapp_url': whatsapp_url
    })

# --- AUTHENTICATION & PROFILE VIEWS ---

def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:profile_dashboard')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('shop:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'shop/account/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:profile_dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('shop:product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('shop:product_list')

@login_required
def profile_dashboard(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('shop:profile_dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'shop/account/dashboard.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# --- WISHLIST VIEWS ---

@login_required
def wishlist_detail(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'shop/wishlist/detail.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f'{product.name} was added to your wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.info(request, f'{product.name} was removed from your wishlist.')
    return redirect('shop:wishlist_detail')