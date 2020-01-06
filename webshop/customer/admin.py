from django.contrib import admin
from .models import Complainment

@admin.register(Complainment)
class ComplainAdmin(admin.ModelAdmin):
	pass
