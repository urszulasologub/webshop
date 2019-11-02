from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import Profile


class LoginForm(forms.Form):
	login = forms.CharField()
	hasło = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
	first_name = forms.CharField(label="Imię", max_length=30, help_text='Wymagane.')
	last_name = forms.CharField(label="Nazwisko", max_length=30, help_text='Wymagane.')
	email = forms.EmailField(label="Email", max_length=254, help_text='Wymagane.')
	birthday = forms.DateField(label="Data urodzenia", help_text='Wymagane. Format: YYYY-mm-dd')  # chyba

	hasło = forms.CharField(label='Hasło', widget=forms.PasswordInput, validators=[validate_password])
	hasło2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput, validators=[validate_password])

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'birthday', 'email')

	def clean_hasło2(self):
		cd = self.cleaned_data
		if cd['hasło'] != cd['hasło2']:
			raise forms.ValidationError('Hasła są różne.')
		return cd['hasło2']

	def clean_birthday(self):
		birthday = self.cleaned_data['birthday']
		'''try:
			birthday = datetime.strptime(date, '%d-%m-%Y')
		except ValueError:
			raise forms.ValidationError('Podaj poprawną datę.')
		'''
		if date.today() <= birthday:
			raise forms.ValidationError('Data jest z przyszłości.')
		return birthday
