from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', views.random_products, name='main'),
	path('products/', views.product_list, name='product_list'),
	path('<int:page>/', views.product_list, name='product_list'),
	path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
	path('<slug:category_slug>/<int:page>/', views.product_list, name='product_list_by_category'),
	path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
	path('delete_review/<int:id>', views.delete_review, name='delete_review'),
	path('searching', views.searching, name='searching'),
]
