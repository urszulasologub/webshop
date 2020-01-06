from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cart.models import Order, OrderComponent
from django.utils import timezone
from .forms import ComplainForm
from django.http import HttpResponse
from .models import Complainment


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


def make_complainment(request):
	#user = get_object_or_404(User, id=request.user.id)
	user = None
	form = ComplainForm()
	message = None
	if request.user.is_authenticated:
		user = request.user
	else:
		message = 'Tylko zalogowani uzytkownicy mogą wysyłać reklamacje'
		return render(request, 'customer/complain.html', {'form': form, 'message': message })
	if request.method == "POST":
		form = ComplainForm(request.POST)
		if form.is_valid():
			form = form.cleaned_data
			body = form['body']
			email = form['email']
			order_id = form['order_id']
			comp = Complainment.objects.create(user=user, body=body, email=email, order_id=order_id)
			message = 'Wysłano wiadomość. Odpowiedź otrzymasz na adres: %s' % email
			return render(request, 'customer/complain.html', {'form': form, 'message': message })
	return render(request, 'customer/complain.html', {'form': form, 'message': message })
