from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class LoginForm(forms.Form):
	login = forms.CharField()
	hasło = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
	first_name = forms.CharField(label="Imię", max_length=30, help_text='Wymagane.')
	last_name = forms.CharField(label="Nazwisko", max_length=30, help_text='Wymagane.')

	DAYS_CHOICES = [(i, str(i)) for i in range(1, 32)]
	MONTHS_CHOICES = (
		(1, 'Styczeń'),
		(2, 'Luty'),
		(3, 'Marzec'),
		(4, 'Kwiecień'),
		(5, 'Maj'),
		(6, 'Czerwiec'),
		(7, 'Lipiec'),
		(8, 'Sierpień'),
		(9, 'Wrzesień'),
		(10, 'Październik'),
		(11, 'Listopad'),
		(12, 'Grudzień'),
	)
	YEARS_CHOICES = [(i, str(i)) for i in range(1900, 2100)]  # rok się zmieni

	day = forms.TypedChoiceField(label="Dzień", choices=DAYS_CHOICES)
	month = forms.TypedChoiceField(label="Miesiąc", choices=MONTHS_CHOICES)
	year = forms.TypedChoiceField(label="Rok", choices=YEARS_CHOICES)

	email = forms.EmailField(label="Email", max_length=254, help_text='Wymagane.')
	hasło = forms.CharField(label='Hasło', widget=forms.PasswordInput, validators=[validate_password])
	hasło2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput, validators=[validate_password])

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'day', 'month', 'year', 'email')

	def clean_hasło2(self):
		cd = self.cleaned_data
		if cd['hasło'] != cd['hasło2']:
			raise forms.ValidationError('Hasła są różne.')
		return cd['hasło2']

	def validate_birthday(self):
		day = self.cleaned_data['day']
		month = self.cleaned_data['month']
		year = self.cleaned_data['year']
		try:
			birthday = datetime(year=int(year), month=int(month), day=int(day))
		except ValueError:
			self.add_error('day', 'Wybierz poprawną datę.')
			return "01-01-0001"
		if datetime.today() <= birthday:
			self.add_error('day', 'Data jest z przyszłości.')
			return "01-01-0001"
		return birthday
