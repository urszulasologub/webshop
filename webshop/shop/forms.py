from dal import autocomplete
from django import forms
from django.contrib.auth.models import User
from .models import Review, Parameter, Description, Product


class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('body', 'rating', )


class DescriptionForm(forms.ModelForm):
	class Meta:
		model = Description
		fields = ('__all__')
		widgets = {
			'parameter': autocomplete.ListSelect2(url='parameter-autocomplete'
												  #, forward=['product']
													)
		}
