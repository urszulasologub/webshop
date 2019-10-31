from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.product_list, name='product_list'),
	path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
	path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
	# path('account/', include('account.urls')),
	path('delete_review/<int:id>', views.delete_review, name='delete_review'),
]
