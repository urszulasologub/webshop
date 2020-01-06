from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import DeliveryType, Order, OrderComponent
from staff.admin import order_pdf


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
	pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_filter = ['is_sent', 'is_confirmed']
	list_display = ['__str__', 'is_confirmed', 'is_sent', order_pdf]
	pass


@admin.register(OrderComponent)
class OrderComponentAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'is_completed']
	pass
