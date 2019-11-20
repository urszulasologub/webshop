from cart.models import DeliveryType
from shop.models import Product

class Delivery():

	def __init__(self, price=0.0):
		self.products = []
		self.delivery_name = DeliveryType.objects.get(pk=1).name
		self.delivery_price = DeliveryType.objects.get(pk=1).price
		self.price = price


	def set_delivery(self, id):
		self.delivery_name = DeliveryType.objects.get(pk=id).name
		self.delivery_price = DeliveryType.objects.get(pk=id).price
	

	def get_price(self):
		return self.price


	def get_delivery_price(self):
		return self.delivery_price


	def get_total_price(self):
		return self.price + self.delivery_price