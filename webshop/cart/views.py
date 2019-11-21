from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, ChooseDeliveryType, AddressForm
from cart.models import DeliveryType
from cart.delivery import Delivery
from cart.paypal_payment import *
from cart.models import Order
from django.http import Http404
from django.contrib.auth.decorators import login_required

@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product,
				quantity=cd['ilość'],
				update_quantity=cd['update'])
	return redirect('cart:cart_detail')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart:cart_detail')


def cart_detail(request):
	cart = Cart(request)
	delivery_form = None
	if request.user.is_authenticated:
		delivery_form = ChooseDeliveryType(request.POST)
		if delivery_form.is_valid():
			choice = request.POST.copy()
			choice = int(choice.get('delivery_type'))
			delivery = Delivery(cart.get_total_price())
			delivery.set_delivery(choice)
			new_order = Order(user=request.user, is_confirmed=False, price=cart.get_total_price(), delivery_price=delivery.get_delivery_price())
			new_order.save()
			order_id = new_order.id
			return redirect('cart:choose_address', order_id)
	return render(request, 'cart/checkout.html', {'cart': cart, 'delivery_form': delivery_form})


@login_required
def choose_address(request, id):
	address_form = AddressForm(request.POST)
	order = get_object_or_404(Order, id=id)
	if request.user != order.user:
		raise Http404
	else:
		if request.method == "POST" and address_form.is_valid():
			address_form = address_form.cleaned_data
			order.address = str(address_form['street']) + '/' + str(address_form['number'])
			order.city = str(address_form['city'])
			print(str(address_form['postal_code_1']).zfill(2) + '-' + str(address_form['postal_code_2']).zfill(3) + '\n\n\n')
			order.postal_code = str(address_form['postal_code_1']).zfill(2) + '-' + str(address_form['postal_code_2']).zfill(3)
			order.save()
			return redirect('cart:cart_checkout', id)
	return render(request, 'cart/address.html', {'address_form': address_form, 'order': order})


@login_required
def cart_checkout(request, id):
	cart = Cart(request)
	order = get_object_or_404(Order, id=id)
	if request.method == 'POST':
		return buy_now(request, id)
	return render(request, 'cart/pay.html', {'cart': cart, 'order': order})


@login_required
def buy_now(request, id):
	order = get_object_or_404(Order, id=id)
	if (order.user != request.user):
		raise Http404
	payment = PaypalPayment(request, order.total_price)
	payment_details = payment.make_payment()
	redirection, payment_id = payment.authorize_payment()
	order.payment_id = payment_id
	order.save()
	return redirect(redirection)


@login_required
def finalize(request):
	cart = Cart(request)
	order = None
	message = 'Pomyślnie sfinalizowano transakcję'
	if execute_payment(request) == False:
		message = 'Oczekiwanie na sfinalizowanie traksakcji'
	else:
		order = get_object_or_404(Order, user=request.user, payment_id=str(request.GET.get('paymentId', None)))
		order.is_confirmed = True
		order.save()
		cart.clear()
	return render(request, 'cart/finalize.html', {'message': message, 'order': order})