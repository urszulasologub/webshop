from django import forms
from .models import DeliveryType, Order

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    ilość = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class ChooseDeliveryType(forms.Form):
	delivery_type = forms.ModelChoiceField(queryset=DeliveryType.objects.all(), widget=forms.RadioSelect, required=True, initial=1)


class AddressForm(forms.Form):
	name = forms.CharField(label='Imię', max_length=100)
	surname = forms.CharField(label='Nazwisko', max_length=100)
	street = forms.CharField(label='Ulica', max_length=170)
	number = forms.CharField(label='Numer', max_length=15)
	city = forms.CharField(label='Miasto', max_length=100)
	postal_code_1 = forms.IntegerField(label='Kod pocztowy 1', min_value=0, max_value=99)
	postal_code_2 = forms.IntegerField(label='Kod pocztowy 2', min_value=0, max_value=999)
