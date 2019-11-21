from django.shortcuts import render
from cart.models import Order, OrderComponent
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect

@staff_member_required
def manage_orders(request):
	orders = Order.objects.all()
	return render(request, 'staff/manage_orders.html', {'orders': orders})


@staff_member_required
def show_order(request, id):
	order = get_object_or_404(Order, id=id)
	components = OrderComponent.objects.filter(order=order)
	return render(request, 'staff/show_order.html', {'order': order, 'components': components})