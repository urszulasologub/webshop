from django.shortcuts import render
from cart.models import Order, OrderComponent
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderButtons, FilterButton, AddDeliverySearchingCode
from django.http import HttpResponseRedirect

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
			elif val == 'Lista produktów do skompletowania':
				return show_products(request)
			elif val == 'Opłacone zamówienia do skompletowania':
				conf_orders = Order.objects.filter(is_confirmed=True)
				orders = []
				for order in conf_orders:
					if order.are_products:
						components = OrderComponent.objects.filter(order=order)
						if are_components_completed(components) == False:
							orders.append(order)
	else:
		form = OrderButtons()
	return render(request, 'staff/manage_orders.html', {'orders': orders})


@staff_member_required
def show_order(request, id):
	order = get_object_or_404(Order, id=id)
	if request.method == 'POST':
		form = AddDeliverySearchingCode(request.POST)
		if form.is_valid():
			order.is_sent = True
			order.delivery_searching_code = form.cleaned_data.get('delivery_searching_code')
			order.save()
	else:
		form = AddDeliverySearchingCode()
	components = OrderComponent.objects.filter(order=order)
	return render(request, 'staff/show_order.html', {'order': order, 'components': components, 'form': form })


@staff_member_required
def show_products(request):
	components = OrderComponent.objects.all()
	return render(request, 'staff/component_list.html', {'components': components})


@staff_member_required
def completed_component(request, id):
	component = get_object_or_404(OrderComponent, id=id)
	component.is_completed = True
	component.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''@staff_member_required
def send_order(request, id):
	order = get_object_or_404(Order, id=id)
	if request.method == 'POST':
		form = AddDeliverySearchingCode(request.POST)
		if form.is_valid():
			order.is_sent = True
			order.delivery_searching_code = form.cleaned_data.get('delivery_searching_code')
			order.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))'''


@staff_member_required
def find_order(request):
	form = None
	orders = None
	if request.method == 'POST':
		form = FilterButton(request.POST)
		if form.is_valid():
			order_id = form.cleaned_data.get("order_id")
			orders = Order.objects.filter(id=order_id)
	else:
		form = FilterButton()
	return render(request, 'staff/finder.html', {'form': form, 'orders': orders})