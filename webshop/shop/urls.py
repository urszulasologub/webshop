from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.product_list, name='product_list'),
	path('<int:page>/', views.product_list, name='product_list'),
	path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
	path('<slug:category_slug>/<int:page>/', views.product_list, name='product_list_by_category'),
	path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
	path('delete_review/<int:id>', views.delete_review, name='delete_review'),
	path('searching', views.searching, name='searching'),
	re_path(r'^newsletter/', include('newsletter.urls')),
]
