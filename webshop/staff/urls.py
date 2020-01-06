from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'staff'

urlpatterns = [
	path('orders/', views.manage_orders, name='manage_orders'),
	path('order/<int:id>/', views.show_order, name='show_order'),
	path('completed_component/<int:id>/', views.completed_component, name='completed_component'),
	#path('send_order/<int:id>', views.send_order, name='send_order'),
	path('find_order/', views.find_order, name='find_order'),
	path('refund_order/<int:id>', views.refund_order, name='refund_order'),
	path('complainments', views.read_complainments, name='complainments'),
	path('close_complainment/<int:id>', views.close_complainment, name='close_complainment'),
]
