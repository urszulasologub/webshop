from django.contrib import admin
from .forms import DescriptionForm
from .models import Category, Product, Review, Parameter, Description


class ParameterInline(admin.StackedInline):
	model = Parameter


class DescriptionAdmin(admin.StackedInline):
	model = Description
	#form = DescriptionForm #jeszcze nie działa xd


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}
	inlines = [ParameterInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price', 'available']
	prepopulated_fields = {'slug': ('name',)}
	inlines = [DescriptionAdmin]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ['body', ]
	search_fields = ['body', ]
	list_filter = ['rating', ]
