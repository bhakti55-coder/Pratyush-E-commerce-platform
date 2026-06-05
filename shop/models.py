from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User # Required for linking wishlists to specific users
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=200)
    name_mr = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    # Media Assets
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    video = models.FileField(upload_to='products/videos/%Y/%m/%d', blank=True, null=True, help_text="Upload a product demonstration video")
    
    description = models.TextField(blank=True, help_text="Write only unique details here (e.g., fabric type, design details)")
    
    # Pricing (Only single Price field)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (₹)")
    
    # Inventory controls
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Permanent Global Sections (Pre-filled Defaults)
    product_quality_policy = models.CharField(max_length=255, default="100% Premium Quality Guaranteed")
    shipping_policy = models.CharField(max_length=255, default="🔥 FREE SHIPPING ALL OVER INDIA 🔥")
    return_policy = models.CharField(max_length=255, default="Strict No-Return Policy applies.")
    security_measure = models.CharField(max_length=255, default="Package opening video is compulsory for any damage claims.")
    booking_contact_name = models.CharField(max_length=100, default="Manjushri")
    booking_contact_number = models.CharField(max_length=15, default="8983341944")
    
    # New flexible section for adding any extra numbers, updates, or custom notes easily
    additional_policies_and_notes = models.TextField(blank=True, help_text="Add any extra booking numbers or custom notices here. Each note on a new line.")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    
    # NEW VARIATION FIELD
    color_name = models.CharField(max_length=100, blank=True, null=True, help_text="Color name for this thumbnail variant (e.g., Royal Blue, Ruby Red)")

    def __str__(self):
        return f"{self.color_name or 'Gallery'} Image for {self.product.name}"

# --- NEW WISHLIST MODEL ---
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents a user from adding the same product twice
        unique_together = ('user', 'product') 

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.product.name}"

# --- NEW PROFILE MODEL ---
class Profile(models.Model):
    # Links directly to Django's built-in User model. If the User is deleted, the profile is deleted.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # Custom shipping and contact fields matching our delivery requirements
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    house_no_flat = models.CharField(max_length=255, blank=True, null=True, verbose_name="House No / Flat")
    address_street = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address / Street")
    landmark = models.CharField(max_length=255, blank=True, null=True, verbose_name="Near By Landmark")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="City Name")
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name="District")
    state = models.CharField(max_length=100, blank=True, null=True, verbose_name="State")
    pincode = models.CharField(max_length=10, blank=True, null=True, verbose_name="Pin Code")

    def __str__(self):
        return f"Profile for {self.user.username}"

# --- SIGNALS TO AUTO-CREATE PROFILE ---
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically creates a Profile instance whenever a new User instance is saved."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """Ensures the profile is updated whenever the User instance is saved.
    Safely catches old users who don't have a profile and creates one for them."""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # If the profile doesn't exist for an old user, create it now!
        Profile.objects.create(user=instance)