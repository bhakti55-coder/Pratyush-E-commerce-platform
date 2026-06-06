from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),
    
    # 2. Cart App Routes (Must be above shop routes to prevent slug collisions)
    path('cart/', include('cart.urls', namespace='cart')), 
    
    # 3. Main Shop App Routes
    path('', include('shop.urls', namespace='shop')), 
]

# Serves user-uploaded media files (like product images) during local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)