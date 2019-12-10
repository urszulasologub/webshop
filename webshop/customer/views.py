from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cart.models import Order, OrderComponent
from django.utils import timezone


@login_required
def show_profile(request):
	user = get_object_or_404(User, id=request.user.id)
	return render(request, 'customer/profile.html', {'user': user})


@login_required
def show_orders(request):
	user = get_object_or_404(User, id=request.user.id)
	orders = Order.objects.filter(user=user)
	for order in orders:			#we need to delete every deprecated order
		if (order.is_confirmed == False and order.expiration_date < timezone.now()) or order.are_products == False:
			order.delete()
	orders = Order.objects.filter(user=user).order_by('-created_at')
	order_components = []
	for order in orders:
		components = OrderComponent.objects.filter(order=order)
		for component in components:
			order_components.append(component)
	return render(request, 'customer/orders.html', {'orders': orders, 'components': order_components})
