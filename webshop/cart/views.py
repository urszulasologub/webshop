from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm, ChooseDeliveryType

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
	choice = None
	if delivery_form.is_valid():		#need to finish this
		choice = delivery_form.save(commit=False)
		choice.save()
	return render(request, 'cart/checkout.html', {'cart': cart, 'delivery_form': delivery_form})


def payment_choice(request):
	cart = Cart(request)
	return render(request, 'cart/pay.html', {'cart': cart} )