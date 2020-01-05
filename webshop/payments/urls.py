from django.conf.urls import url, include, path
from . import views

app_name = 'payments'

urlpatterns = [
	url('paypal/', include('paypal.standard.ipn.urls')),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
]