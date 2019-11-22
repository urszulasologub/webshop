
from django import forms
from cart.models import Order

class OrderButtons(forms.Form):
    btn = forms.CharField()


class FilterButton(forms.Form):
	order_id = forms.IntegerField(min_value=0)


class AddDeliverySearchingCode(forms.Form):
	delivery_searching_code = forms.CharField(max_length=200)