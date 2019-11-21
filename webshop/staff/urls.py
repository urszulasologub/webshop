from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'staff'

urlpatterns = [
	path('orders/', views.manage_orders, name='manage_orders'),
	path('order/<int:id>/', views.show_order, name='show_order'),
]
