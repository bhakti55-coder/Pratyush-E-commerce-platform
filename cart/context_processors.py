from .cart import Cart

def cart(request):
    """
    Instantiates the cart and makes it available to all templates globally.
    """
    return {'cart': Cart(request)}