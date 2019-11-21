from django.contrib import admin
from .models import DeliveryType, Order

@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
	pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_filter = ['is_sent', 'is_confirmed', 'is_sent']
	pass
