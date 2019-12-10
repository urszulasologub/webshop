from dal import autocomplete
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Category, Product, Review, Description, Parameter, ExtraPhoto
from .forms import ReviewForm#, DescriptionForm
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from statistics import mean
import operator
from collections import OrderedDict
from django.core.paginator import Paginator


def product_list(request, category_slug=None, page=1):
	category = None
	categories = Category.objects.all()
	product_list = Product.objects.filter(available=True)
	paginator = Paginator(product_list, 12)
	dictionary = None
	dictionary = {} 
	for product in product_list:
		parameters = Description.objects.filter(product=product)
		dictionary[product] = parameters
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		product_list = product_list.filter(category=category)
	products = paginator.get_page(page)
	return render(request, 'shop/product/list.html',
				  {'category': category, 'categories': categories, 'products': products, 'dictionary': dictionary, 'paginator': paginator })


@login_required
def add_review(request, new_review, product):
	review_form = ReviewForm(data=request.POST)
	if review_form.is_valid:
		new_review = review_form.save(commit=False)
		new_review.product = product
		new_review.user = request.user
		new_review.save()
	return new_review, review_form


def reviews_by_user_count(request, product):
	return Review.objects.filter(user=request.user, product=product).count()


def product_detail(request, id, slug):
	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	descriptions = Description.objects.all()
	descriptions = descriptions.filter(product=product)
	cart_product_form = CartAddProductForm()
	reviews = product.review.filter(active=True)
	new_review = None
	users_reviews = None
	if request.user.is_authenticated:
		users_reviews = reviews_by_user_count(request, product)
	if request.method == 'POST' and users_reviews < 1:
		new_review, review_form = add_review(request, new_review, product)
	else:
		review_form = ReviewForm()
	recommendations = choose_recommended(request, product.category, 5)

	if not 'recent' in request.session or not request.session['recent']:
		request.session['recent'] = [id]
		show_recent = None
	else:
		show_recent = [Product.objects.get(id=id) for id in request.session['recent']]
		recent = request.session['recent']
		if id in recent:
			recent.remove(id)
		recent.insert(0, id)
		if len(recent) > 5:
			recent.pop()
		request.session['recent'] = recent
	extra_photos = ExtraPhoto.objects.filter(product=product)
	return render(request, 'shop/product/detail.html', {'product': product,
														'cart_product_form': cart_product_form,
														'descriptions': descriptions,
														'reviews': reviews,
														'new_review': new_review,
														'review_form': review_form,
														'users_reviews': users_reviews,
														'recommendations': recommendations,
														'recent': show_recent,
														'extra_photos': extra_photos})


@login_required
def delete_review(request, id):
	review = get_object_or_404(Review, id=id)
	product_id = review.product.id
	product_slug = review.product.slug
	review.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ParameterAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		#if not self.request.user.is_aunthenticated():
		#	return Description.objects.none()

		qs = Description.objects.all()
		'''#pqs = Parameter.objects.all()

		#product = self.forwarded.get('product', None)
		#parameters = self.forward.get('category', None)

		#category = product.get('category')

		#if product:
		#	pqs = pqs.filter(category)
		#	qs = qs.filter(product)'''

		if self.q:
			#pqs = pqs.filter()
			qs = qs.filter(parameter__name__startswith=self.q)

		return qs


def choose_recommended(request, category, amount):
	products = Product.objects.filter(category=category)
	dict = {}
	for product in products:
		if product.average_rating != None and product.average_rating > 2.5:
			dict[product] = product.average_rating
	dictionary = OrderedDict(sorted(dict.items(), key=operator.itemgetter(1), reverse=True))
	recommended_products = []
	i = 0
	for product in dictionary:
		recommended_products.append(product)
		i += 1
		if (i == amount):
			break
	return recommended_products
