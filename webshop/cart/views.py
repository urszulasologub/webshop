from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, ChooseDeliveryType
from cart.models import DeliveryType
from cart.order import Delivery
from cart.paypal_payment import PaypalPayment
from cart.models import Payments

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
	delivery_form = ChooseDeliveryType(request.POST)
	if delivery_form.is_valid():
		choice = request.POST.copy()
		choice = int(choice.get('delivery_type'))
		delivery = Delivery(cart.get_total_price())
		delivery.set_delivery(choice)
		return cart_checkout(request, cart, delivery)
	return render(request, 'cart/checkout.html', {'cart': cart, 'delivery_form': delivery_form})


def cart_checkout(request, cart, delivery):
	#cart = Cart(request)
	return render(request, 'cart/pay.html', {'cart': cart, 'delivery': delivery})


def buy_now(request):
	payment = PaypalPayment(request)
	payment.make_payment()
	redirection = payment.authorize_payment()
	return redirect(redirection)

