from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """Initialize the shopping cart using Django sessions."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart dictionary in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, color='Default Base Color'):
        """Add a product variant to the cart or update its quantity."""
        product_id = str(product.id)
        # 🛡️ COMPOSITE KEY TRICK: Create a unique identifier combining item ID and color
        item_key = f"{product_id}_{color}"

        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.price),
                'product_id': product_id,
                'color': color
            }

        if override_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
            
        self.save()

    def save(self):
        """Mark the session as modified to guarantee it saves to the database."""
        self.session.modified = True

    def remove(self, product, color=None):
        """Remove a specific product variant from the cart completely."""
        product_id = str(product.id)
        # If no color passed, fallback gracefully, but target matching composite keys
        color_variant = color if color else 'Default Base Color'
        item_key = f"{product_id}_{color_variant}"

        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        """Loop through the items in the cart and fetch associated Product objects from DB."""
        item_keys = self.cart.keys()
        # Extract all raw database primary keys from our composite session keys
        product_ids = [item['product_id'] for item in self.cart.values()]
        
        # Batch query all products at once for optimized database efficiency
        products = Product.objects.filter(id__in=product_ids)
        
        # Map product objects by their ID for easy lookups
        product_map = {str(p.id): p for p in products}

        # Deep copy cart to prevent mutation side-effects during iteration loops
        cart_copy = {k: v.copy() for k, v in self.cart.items()}

        for item_key, item in cart_copy.items():
            # Attach the real database model object to the temporary template loop item
            item['product'] = product_map.get(item['product_id'])
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count the total quantity of all collective individual items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the total basket cost of all combined product rows."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Completely empty the shopping cart session data."""
        del self.session[settings.CART_SESSION_ID]
        self.save()