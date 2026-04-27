from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='addcart'),
    path('display_cart/', views.display_cart, name='displaycart'),
    path('update/', views.update_cart, name='updatecart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
]