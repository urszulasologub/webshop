from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, ChooseDeliveryType
from cart.models import DeliveryType
from django.http import HttpResponseRedirect

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
		delivery = DeliveryType.objects.get(pk=choice)
		price = delivery.price
		cart.set_delivery_price(price)
		print('CHUJ\n\n\n')
		print(cart.get_delivery_price())
		return render(request, 'cart/pay.html', {'cart': cart})
	return render(request, 'cart/checkout.html', {'cart': cart, 'delivery_form': delivery_form})


def payment_choice(request):
	cart = Cart(request)
	return render(request, 'cart/pay.html', {'cart': cart})