from django import forms
from .models import DeliveryType

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    ilość = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)


class ChooseDeliveryType(forms.Form):
	sposób_dostawy = forms.ModelChoiceField(queryset=DeliveryType.objects.all(), widget=forms.RadioSelect, required=True, initial=1)