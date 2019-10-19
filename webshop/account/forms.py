from django import forms

class LoginForm(forms.Form):
	login = forms.CharField()
	hasło = forms.CharField(widget=forms.PasswordInput)
