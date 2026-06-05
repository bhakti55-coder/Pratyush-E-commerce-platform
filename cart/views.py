from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from urllib.parse import quote
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    """View to handle adding an item to the cart via a form submission."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        cd = form.cleaned_data
        
        # 🛡️ VERIFIED FIX: Grab 'color' directly from request.POST since it's 
        # a manual HTML radio input group rather than a native Django form field.
        selected_color = request.POST.get('color', 'Default Base Color')
        
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
            color=selected_color  # Captures the accurate selected color variant
        )
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    """View to handle removing an individual item completely."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Pulls specific color from URL query params if available (e.g., ?color=Royal Blue)
    color = request.GET.get('color')
    cart.remove(product, color=color)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """Renders the final summary layout page showing items, quantities, and prices."""
    cart = Cart(request)
    
    # Loop over the cart items to attach a working update quantity form to each row
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True,
            'color': item.get('color', 'Default Base Color')  # Keeps color locked during updates
        })
        
    # 1. Base Welcome greeting line
    msg = "Hello! I would like to order from your store:\n\n"
    
    # 2. Compile each cart product along with its direct absolute link on your store
    for item in cart:
        product = item['product']
        # Build the live domain routing link
        product_url = request.build_absolute_uri(product.get_absolute_url())
        
        # 🛡️ VERIFIED FIX: Replaced unicode bullet points with web-safe standard text dashes/emojis
        # This completely resolves the annoying '?' encoding glitch on WhatsApp Web and Mobile!
        msg += f"📦 *{product.name}*\n"
        msg += f"   - Color: {item.get('color', 'Default Base Color')}\n"
        msg += f"   - Quantity: {item['quantity']}\n"
        msg += f"   - Total: ₹{item['total_price']}\n"
        msg += f"   - Link: {product_url}\n\n"
        
    # 3. Add the overall subtotal calculation
    msg += f"*Total Amount:* ₹{cart.get_total_price()}\n\n"
    
    # 4. Inject the empty shipping credentials template for the user to complete
    # Uses standard text dashes which never fail to compile in URL routing links
    msg += "✍️ *SHIPPING & DELIVERY DETAILS:*\n"
    msg += " - Customer Name: \n"
    msg += " - House No / Flat: \n"
    msg += " - Address / Street: \n"
    msg += " - Near By Landmark: \n"
    msg += " - City Name: \n"
    msg += " - District: \n"
    msg += " - State: \n"
    msg += " - Pin Code: \n"
    msg += " - Phone No: \n"

    # Safely convert the string spaces and symbols into valid URL format
    encoded_msg = quote(msg)
    
    # Official WhatsApp Send Routing Link (opens user's personal chat client directly)
    whatsapp_url = f"https://wa.me/918983341944?text={encoded_msg}"
    
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'whatsapp_url': whatsapp_url
    })