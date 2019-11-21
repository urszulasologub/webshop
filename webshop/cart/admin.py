from django.contrib import admin
from .models import DeliveryType, Order, OrderComponent

@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
	pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_filter = ['is_sent', 'is_confirmed']
	list_display = ['__str__', 'price', 'is_confirmed', 'is_sent']
	pass


@admin.register(OrderComponent)
class OrderComponentAdmin(admin.ModelAdmin):
	pass