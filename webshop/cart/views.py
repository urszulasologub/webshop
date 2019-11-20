from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, ChooseDeliveryType
from cart.models import DeliveryType
from cart.delivery import Delivery
from cart.paypal_payment import PaypalPayment
from cart.models import Order
from django.http import Http404

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
		new_order = Order(user=request.user, is_confirmed=False, price=cart.get_total_price(), delivery_price=delivery.get_delivery_price())
		new_order.save()
		order_id = new_order.id
		return redirect('cart:cart_checkout', order_id)
	return render(request, 'cart/checkout.html', {'cart': cart, 'delivery_form': delivery_form})


def cart_checkout(request, id):
	cart = Cart(request)
	order = get_object_or_404(Order, id=id)
	if request.method == 'POST':
		return buy_now(request, id)
	return render(request, 'cart/pay.html', {'cart': cart, 'order': order})


def buy_now(request, id):
	order = get_object_or_404(Order, id=id)
	if (order.user != request.user):
		raise Http404
	payment = PaypalPayment(request, order.total_price)
	payment.make_payment()
	redirection = payment.authorize_payment()
	return redirect(redirection)

