from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # 🛒 Cart Detail Page: Renders the summary matrix layout and WhatsApp link
    path('', views.cart_detail, name='cart_detail'),
    
    # ➕ Add Item Route: Processes form submissions for item additions and quantity overrides
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    
    # ❌ Remove Item Route: Processes removal requests (targets variants using URL query params)
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]