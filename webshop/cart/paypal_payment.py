import paypalrestsdk
import logging
from .cart import Cart

class PaypalPayment():
	def __init__(self, request, total_price):
		self.price = str(total_price)
		print("\n\n\n\n\n" + self.price + '\n\n\n\n')
		self.request = request
		#self.cart = cart
		paypalrestsdk.configure({
			"mode": "sandbox", # sandbox or live
			"client_id": "AfNoHbwXRtAOBeEcOzPvXLQDsW9ZwQY_2kYRlnmmaHlm1q770zLrxUPZHlmbPwIZXzvM4zmEo63Q7dGs",
			"client_secret": "EFcLsJVDihQlZeS8aYlOoWzcPL_ghf3qWkj69uq3xcNGu6kgNSY7_Wl2yuxnLEzV6cx7fwKAPebsE1Kp" })
		self.payment = paypalrestsdk.Payment({
			"intent": "sale",
			"payer": {
				"payment_method": "paypal"},
			"redirect_urls": {
				"return_url": "http://wykop.pl/",
				"cancel_url": "http://127.0.0.1:8000/"},
			"transactions": [{
				"item_list": {
					"items": [{
						"name": "Zakupy",
						"sku": "Zakupy",
						"price": self.price,
						"currency": "PLN",
						"quantity": 1}]},
				"amount": {
					"total": self.price,
					"currency": "PLN"},
				"description": "Zakup w sklepie internetowym"}]})
	

	def make_payment(self):
		if self.payment.create():
			print("Payment created successfully")
		else:
			print(self.payment.error)


	def authorize_payment(self):
		for link in self.payment.links:
			if link.rel == "approval_url":
				approval_url = str(link.href)
				print("Redirect for approval: %s" % (approval_url))
		return (approval_url)

	
	def execute_payment(self):
		payment = paypalrestsdk.Payment.find(str(self.request.GET.get('paymentId', None)))
		if payment.execute({"payer_id": str(self.request.GET.get('PayerID', None))}):
			print("Payment execute successfully")
		else:
			print(payment.error)

