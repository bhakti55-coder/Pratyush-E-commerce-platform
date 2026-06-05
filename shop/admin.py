# shop/admin.py
from django.contrib import admin
from .models import Category, Product, ProductImage, Wishlist, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_mr', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5  # Provides 5 blank image fields automatically by default


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    
    inlines = [ProductImageInline]
   
    fieldsets = [
        ('Core Details', {
            'fields': ['category', 'name', 'slug', 'description']
        }),
        ('Media Assets', {
            'fields': ['image', 'video']
        }),
        ('Pricing & Availability', {
            'fields': ['price', 'available']
        }),
        ('Permanent Global Information (Defaults Pre-set)', {
            'fields': [
                'product_quality_policy', 
                'shipping_policy', 
                'return_policy', 
                'security_measure', 
                'booking_contact_name', 
                'booking_contact_number',
                'additional_policies_and_notes'  # Integrated right here for quick extensions
            ],
        }),
    ]

# Registering the new Wishlist model
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'added_date']
    search_fields = ['user__username', 'product__name']

# Registering the new Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'state', 'pincode']
    search_fields = ['user__username', 'user__email', 'phone_number', 'city']