from django import forms
from cart.models import cart


class CartFrom(forms.ModelForm):
    class Meta:
        models=cart
        fields=['food_namee','price','Qty']