from django import forms


class ComplainForm(forms.Form):
	body = forms.CharField(widget=forms.Textarea)
	email = forms.EmailField(label='Email')
	order_id = forms.IntegerField(label='Numer zamówienia (bez zer wiodących)', min_value=0, required=False)