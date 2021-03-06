import paypalrestsdk
from paypalrestsdk import Sale
import logging

logging.basicConfig(level=logging.INFO)

ID = "AfNoHbwXRtAOBeEcOzPvXLQDsW9ZwQY_2kYRlnmmaHlm1q770zLrxUPZHlmbPwIZXzvM4zmEo63Q7dGs"
SID = "EFcLsJVDihQlZeS8aYlOoWzcPL_ghf3qWkj69uq3xcNGu6kgNSY7_Wl2yuxnLEzV6cx7fwKAPebsE1Kp" 

class PaypalPayment():
	def __init__(self, request, total_price):
		self.price = str(total_price)
		self.request = request
		paypalrestsdk.configure({
			"mode": "sandbox", # sandbox or live
			"client_id": ID,
			"client_secret": SID
		})
		'''self.experience = paypalrestsdk.WebProfile({
			"name": "webshop",
			"presentation": {
				"brand_name": "Webshop: sklep Internetowy",
				"locale_code": "PL"
			},
			"input_fields": {
				"no_shipping": 1,
				"address_override": 1
			}
		})
		if not self.experience.create():
			print(self.experience.error)
		else: 
			print(self.experience.id)
			print('\n\n\n\n\n')'''
		exp_id = 'XP-HUNU-U6ZB-HXCB-DQ9R'
		self.payment = paypalrestsdk.Payment({
			"intent": "sale",
			"experience_profile_id": exp_id,
			"payer": {
				"payment_method": "paypal"},
			"redirect_urls": {
				"return_url": "http://127.0.0.1:8000/cart/finalize",
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
				"description": "Zakup w sklepie internetowym"}], 
		})


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
				return (approval_url), self.payment.id
		return None

	
def execute_payment(request):
	payment_id = str(request.GET.get('paymentId', None))
	payer_id =  str(request.GET.get('PayerID', None))
	payment = paypalrestsdk.Payment.find(payment_id)
	if payment.execute({"payer_id": payer_id }):
		return True
	else:
		return False


def make_refund(pay_id):
	paypalrestsdk.configure({
		"mode": "sandbox", # sandbox or live
		"client_id": ID,
		"client_secret": SID
	})
	payment = paypalrestsdk.Payment.find(pay_id)
	sale_id = payment.transactions[0].related_resources[0].sale.id
	sale = Sale.find(sale_id)
	refund = sale.refund({})

	if refund.success():
		print("Refund[%s] Success" % (refund.id))
	else:
		raise Exception('Unable to refund: %s' % refund.error)