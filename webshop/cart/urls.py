from django.urls import path, include
from . import views
from django.conf.urls import url

app_name = 'cart'

urlpatterns = [
    path('checkout/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
	path('cart_checkout/', views.cart_checkout, name='cart_checkout'),
	path('buy_now/', views.buy_now, name='buy_now'),
]
