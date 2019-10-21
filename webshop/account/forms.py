from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
	login = forms.CharField()
	hasło = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
	hasło = forms.CharField(label='Hasło', widget=forms.PasswordInput)
	hasło2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['hasło'] != cd['hasło2']:
			raise forms.ValidationError('Hasła są różne.')
		return cd['hasło2']
