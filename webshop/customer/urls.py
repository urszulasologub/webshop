from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'profile'

urlpatterns = [
	path('show/', views.show_profile, name='show_profile'),
	path('orders/', views.show_orders, name='show_orders'),
]
