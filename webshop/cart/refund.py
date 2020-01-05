# SaleRefund Sample
# This sample code demonstrate how you can
# process a refund on a sale transaction created
# using the Payments API.
# API used: /v1/payments/sale/{sale-id}/refund

from paypalrestsdk import Sale
import logging

logging.basicConfig(level=logging.INFO)


def make_refund(sale_num):
	#sale = Sale.find("7DY409201T7922549")
	sale = Sale.find(sale_num)

	refund = sale.refund({
		"amount": {
			"currency": "PLN"}})

	if refund.success():
		print("Refund[%s] Success" % (refund.id))
		return True
	else:
		print("Unable to Refund")
		print(refund.error)
		return False