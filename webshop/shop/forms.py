from django import forms
from django.contrib.auth.models import User
from .models import Review

class ReviewForm(forms.ModelForm):
	class Meta:
		model = Review
		fields = ('body', 'rating', )
