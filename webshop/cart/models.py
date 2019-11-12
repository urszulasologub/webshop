from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class DeliveryType(models.Model):
	name = models.CharField(max_length=100, unique=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
	description = models.CharField(max_length=300)

	def __str__(self):
		return self.name + ' (' + self.description + ')' + ' - ' + str(self.price) + ' PLN'
