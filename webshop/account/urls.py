from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
	#path('login/', auth_views.LoginView.as_view(), name='login'),
	#path('login/', views.user_login, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('login/', auth_views.LoginView.as_view(), name='login'),
	#path('activate/<slug:uidb64>/<uuid:token>/', views.activate, name='activate'), #tak nie chce działać
	re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate')
]