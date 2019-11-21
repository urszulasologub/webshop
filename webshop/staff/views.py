from django.shortcuts import render
from cart.models import Order, OrderComponent
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderButtons

def are_components_completed(components):
	if components != None:
		for component in components:
			if component.is_completed == False:
				return False
	return True

@staff_member_required
def manage_orders(request):
	orders = Order.objects.all()
	if request.method == 'POST':
		form = OrderButtons(request.POST)
		if form.is_valid():
			val = form.cleaned_data.get("btn")
			if val == 'Opłacone zamówienia':
				orders = Order.objects.filter(is_confirmed=True)
			elif val == 'Skompletowane zamówienia':
				all_orders = Order.objects.filter()
				orders = []
				for order in all_orders:
					if order.are_products:
						components = OrderComponent.objects.filter(order=order)
						if are_components_completed(components):
							orders.append(order)
			elif val == 'Wszystkie zamówienia':
				orders = Order.objects.all()
			elif val == 'Wysłane zamówienia':
				orders = Order.objects.filter(is_sent=True)
	else:
		form = OrderButtons()
	return render(request, 'staff/manage_orders.html', {'orders': orders})


@staff_member_required
def show_order(request, id):
	order = get_object_or_404(Order, id=id)
	components = OrderComponent.objects.filter(order=order)
	return render(request, 'staff/show_order.html', {'order': order, 'components': components})