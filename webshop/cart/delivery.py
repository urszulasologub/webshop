from cart.models import DeliveryType
from shop.models import Product

class Delivery():

	def __init__(self, price=0.0, free_delivery_price=500):
		self.delivery_name = DeliveryType.objects.get(pk=1).name
		self.delivery_price = DeliveryType.objects.get(pk=1).price
		self.price = price
		self.is_delivery_free = False
		self.set_price_to_get_free_delivery(free_delivery_price)


	def set_price_to_get_free_delivery(self, amount):
		if self.price >= amount:
			self.is_delivery_free = True


	def set_delivery(self, id):
		self.delivery_name = DeliveryType.objects.get(pk=id).name
		if self.is_delivery_free == False:
			self.delivery_price = DeliveryType.objects.get(pk=id).price
		else:
			self.delivery_price = 0


	def get_delivery_price(self):
		return self.delivery_price


	def get_total_price(self):
		return self.price + self.delivery_price