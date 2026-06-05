import urllib.parse  
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Wishlist 
from cart.forms import CartAddProductForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm

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
    
    # 1. Initialize variables for pre-filling the WhatsApp message
    cust_name = ""
    house = ""
    street = ""
    landmark = ""
    city = ""
    district = ""
    state = ""
    pin = ""
    phone = ""

    # 2. If the user is logged in, attempt to fetch their profile data
    if request.user.is_authenticated:
        # We use a try-except block just in case a user exists without a profile
        try:
            profile = request.user.profile
            cust_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            house = profile.house_no_flat or ""
            street = profile.address_street or ""
            landmark = profile.landmark or ""
            city = profile.city or ""
            district = profile.district or ""
            state = profile.state or ""
            pin = profile.pincode or ""
            phone = profile.phone_number or ""
        except:
            pass # Fails silently if no profile exists; variables remain blank
    
    # 3. Create the clean text string, inserting the user's data if available
    whatsapp_message = (
        f"Hello! I would like to order from your store:\n\n"
        f"🛍️ *{product.name}*\n"
        f" - Color: Default Base Color\n"
        f" - Quantity: 1\n"
        f" - Total: ₹{product.price}\n"
        f" - Link: {request.build_absolute_uri()}\n\n"
        f"*Total Amount:* ₹{product.price}\n\n"
        f"📋 *SHIPPING & DELIVERY DETAILS:*\n"
        f" - Customer Name: {cust_name}\n"
        f" - House No / Flat: {house}\n"
        f" - Address / Street: {street}\n"
        f" - Near By Landmark: {landmark}\n"
        f" - City Name: {city}\n"
        f" - District: {district}\n"
        f" - State: {state}\n"
        f" - Pin Code: {pin}\n"
        f" - Phone No: {phone}"
    )
    
    # 4. Convert text to a safe URL format
    encoded_message = urllib.parse.quote(whatsapp_message)
    whatsapp_url = f"https://api.whatsapp.com/send/?phone=918983341944&text={encoded_message}"
    
    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'whatsapp_url': whatsapp_url  
    })

# --- WISHLIST VIEWS ---

@login_required(login_url='/login/')
def wishlist_detail(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/wishlist/detail.html', {'wishlist_items': wishlist_items})

@login_required(login_url='/login/')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"{product.name} was added to your wishlist!")
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))

@login_required(login_url='/login/')
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.info(request, f"{product.name} was removed from your wishlist.")
    return redirect('shop:wishlist_detail')

# --- AUTHENTICATION & PROFILE VIEWS ---

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save() # This triggers your signal and automatically creates the Profile!
            login(request, new_user)
            messages.success(request, f"Welcome {new_user.first_name}! Your account has been created.")
            return redirect('shop:product_list')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'shop/account/register.html', {'user_form': user_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('shop:product_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'shop/account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('shop:product_list')

@login_required(login_url='/login/')
def profile_dashboard(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your shipping details have been updated successfully.')
            return redirect('shop:profile_dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'shop/account/dashboard.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })