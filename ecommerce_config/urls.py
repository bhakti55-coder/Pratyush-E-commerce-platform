# ecommerce_config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')), # Connect your cart namespace!
    path('', include('shop.urls', namespace='shop')), # Connects your shop app to the main root URL
]

# This tells Django to serve uploaded images/videos while we are developing locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)