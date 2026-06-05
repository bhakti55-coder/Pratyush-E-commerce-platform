from .cart import Cart

def cart(request):
    """Exposes the active cart instance globally across all template contexts."""
    return {'cart': Cart(request)}