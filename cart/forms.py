from django import forms

# Generates selectable drop-down limits (1 to 10 items)
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddProductForm(forms.Form):
    """Form to handle adding items to the cart and updating quantities smoothly."""
    
    # Dropdown menu to pick quantity (1-10 pieces) with clean Bootstrap classes built-in
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label='Qty',
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm d-inline-block w-auto ms-2'
        })
    )
    
    # Hidden flag indicating whether to accumulate quantities or overwrite them (for cart updates)
    override = forms.BooleanField(
        required=False, 
        initial=False, 
        widget=forms.HiddenInput
    )
    
    # 🛡️ VERIFIED VARIANT TRACKING: Hidden input field that safely holds and binds 
    # the selected color string during form rendering and cleaning sequences.
    color = forms.CharField(
        required=False, 
        initial='Default Base Color', 
        widget=forms.HiddenInput
    )