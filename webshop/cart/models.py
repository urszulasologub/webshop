from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User


class DeliveryType(models.Model):
	name = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.name + ' (' + self.description + ')' + ' - ' + str(self.price) + ' PLN'


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING) 
	is_confirmed = models.BooleanField(default=False)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	delivery_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
	payment_id = models.CharField(max_length=1000, null=True)

	@property
	def total_price(self):
		return self.price + self.delivery_price

	def __str__(self):
		return "#" + str(self.id).zfill(6) + ": " + str(self.user) + ' - ' + str(self.price + self.delivery_price) + " PLN"