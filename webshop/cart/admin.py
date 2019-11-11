from django.contrib import admin
from .models import DeliveryType

@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
	pass
