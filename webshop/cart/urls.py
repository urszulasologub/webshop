from django.urls import path, include
from . import views
from django.conf.urls import url

app_name = 'cart'

urlpatterns = [
    path('checkout/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
	path('cart_checkout/<int:id>', views.cart_checkout, name='cart_checkout'),
	path('choose_address/<int:id>', views.choose_address, name='choose_address'),
	path('finalize/', views.finalize, name='finalize'),
]
