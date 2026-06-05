from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # 1. Main views
    path('', views.product_list, name='product_list'),
    
    # 2. Account Paths (Must come BEFORE dynamic slugs)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_dashboard, name='profile_dashboard'),
    
    # 3. Wishlist paths (Must come BEFORE dynamic slugs)
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # 4. Dynamic paths (Must come AFTER static paths)
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'), 
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]