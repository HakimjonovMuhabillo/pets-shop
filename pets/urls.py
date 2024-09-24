from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop_view, name='shop'),
    path('product/<slug:slug>/', single_product, name='product'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('account/', account, name='account'),
    path('save_review/<int:pk>/', save_review, name='save_review'),
    path('wishlist_action/<int:pk>/', wishlist_action, name='wishlist_action'),
    path('wishlist/', wishlist, name='wishlist'),
    path('search/', SearchView.as_view(), name='search'),
    path('contact/', contact, name='contact'),

    path('to_cart/<int:product_id>/', to_cart, name='to_cart'),
    path('cart/', cart, name='cart'),
    path('plus_minus/<int:pk>/<str:action>/<str:color>/<str:size>/<int:quantity>', plus_minus, name='plus_minus'),
    path('clear/', clear, name='clear'),
    path('checkout/', checkout, name='checkout'),
    path('process_checkout/', process_checkout, name='process_checkout'),
    path('payment-success/', success_payment, name='success')
]