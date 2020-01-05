from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from shop.models import Product
from coupons.models import Coupon
from .cart import Cart


class DeliveryType(models.Model):
	name = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.name + ' (' + self.description + ')' + ' - ' + str(self.price) + ' PLN'


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING) 
	is_confirmed = models.BooleanField(default=False)
	#price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	delivery_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
	delivery_type = models.CharField(max_length=100)
	payment_id = models.CharField(max_length=1000, null=True)
	name = models.CharField(max_length=100, default="None")
	surname = models.CharField(max_length=100, default="None")
	address = models.CharField(max_length=200, default="None")
	city = models.CharField(max_length=100, default="None")
	postal_code = models.CharField(max_length=6, default="00-000")
	is_sent = models.BooleanField(default=False)
	delivery_searching_code = models.CharField(max_length=200, null=True)
	#are_products = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	expiration_date = models.DateTimeField()
	discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

	@property
	def price(self):
		price = 0
		components = OrderComponent.objects.filter(order=self)
		for component in components:
			price += (component.price * component.quantity)
		return price

	@property
	def are_products(self):
		components = OrderComponent.objects.filter(order=self)
		if not components:
			return False
		return True		

	@property
	def total_price(self):
		return self.price + self.delivery_price - self.discount

	def __str__(self):
		return "#" + str(self.id).zfill(6) + ": " + str(self.user) + ' - ' + str(self.price + self.delivery_price - self.discount) + " PLN"


	@property
	def is_completed(self):
		components = OrderComponent.objects.filter(order=self)
		for component in components:
			if component.is_completed == False:
				return False
		return True


class OrderComponent(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	is_completed = models.BooleanField(default=False)
	quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])

	def full_price(self):
		return self.price * self.quantity

	def __str__(self):
		return "#" + str(self.order.id) + ": "  + str(self.product.name)