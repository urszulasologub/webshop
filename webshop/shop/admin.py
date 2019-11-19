from django.contrib import admin
from .models import Category, Product, Review, Parameter, Description


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price', 'available']
	prepopulated_fields = {'slug': ('name',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ['body', ]
	search_fields = ['body', ]
	list_filter = ['rating', ]


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
	list_display = ['category', 'name']


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
	list_display = ['parameter', 'product', 'description']
	list_editable = ['description']
