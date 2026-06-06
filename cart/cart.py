from decimal import Decimal
from django.conf import settings
from shop.models import Product
from urllib.parse import quote

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, color='Default Base Color'):
        product_id = str(product.id)
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
        self.session.modified = True

    def remove(self, product, color=None):
        product_id = str(product.id)
        color_variant = color if color else 'Default Base Color'
        item_key = f"{product_id}_{color_variant}"

        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(p.id): p for p in products}

        for item_key, item in self.cart.items():
            item['product'] = product_map.get(item['product_id'])
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def generate_whatsapp_message(self, request):
        """Generates the pre-filled text string for WhatsApp."""
        user = request.user
        msg = "Hello! I would like to order from your store:\n\n"
        
        for item in self:
            product = item['product']
            product_url = request.build_absolute_uri(product.get_absolute_url())
            msg += f"📦 *{product.name}*\n"
            msg += f"  - Color: {item.get('color', 'Default Base Color')}\n"
            msg += f"  - Quantity: {item['quantity']}\n"
            msg += f"  - Total: ₹{item['total_price']}\n"
            msg += f"  - Link: {product_url}\n\n"
            
        msg += f"*Total Amount:* ₹{self.get_total_price()}\n\n"
        msg += "✍️ *SHIPPING & DELIVERY DETAILS:*\n"

        if user.is_authenticated and hasattr(user, 'profile'):
            p = user.profile
            msg += f" - Customer Name: {user.first_name} {user.last_name}\n".strip()
            msg += f" - House No / Flat: {p.house_no_flat or ''}\n"
            msg += f" - Address / Street: {p.address_street or ''}\n"
            msg += f" - Near By Landmark: {p.landmark or ''}\n"
            msg += f" - City Name: {p.city or ''}\n"
            msg += f" - District: {p.district or ''}\n"
            msg += f" - State: {p.state or ''}\n"
            msg += f" - Pin Code: {p.pincode or ''}\n"
            msg += f" - Phone No: {p.phone_number or ''}\n"
        else:
            msg += " - [Please fill in your address details here]\n"

        return f"https://wa.me/918983341944?text={quote(msg)}"

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()