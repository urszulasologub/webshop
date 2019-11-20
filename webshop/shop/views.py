from dal import autocomplete
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import Category, Product, Review, Description, Parameter
from .forms import ReviewForm#, DescriptionForm
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count


def product_list(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	return render(request, 'shop/product/list.html',
				  {'category': category, 'categories': categories, 'products': products})


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
	return render(request, 'shop/product/detail.html', {'product': product,
														'cart_product_form': cart_product_form,
														'reviews': reviews,
														'new_review': new_review,
														'review_form': review_form,
														'users_reviews': users_reviews})


@login_required
def delete_review(request, id):
	review = get_object_or_404(Review, id=id)
	product_id = review.product.id
	product_slug = review.product.slug
	review.delete()
	return product_detail(request, product_id, product_slug)


class ParameterAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		#if not self.request.user.is_aunthenticated():
		#	return Description.objects.none()

		qs = Description.objects.all()
		#pqs = Parameter.objects.all()

		#product = self.forwarded.get('product', None)
		#parameters = self.forward.get('category', None)

		#category = product.get('category')

		#if product:
		#	pqs = pqs.filter(category)
		#	qs = qs.filter(product)

		if self.q:
			#pqs = pqs.filter()
			qs = qs.filter(parameter__name__startswith=self.q)

		return qs
