from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm


def user_login(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['login'], password=cd['hasło'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Zalogowano pomyślnie')
				else:
					return HttpResponse('Konto dezaktywowane')
			else: 
				return HttpResponse('Podano nieprawidłowe dane')
		else:
			form = LoginForm()
	return render(request, 'account/login.html', {'form': form})		


def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(
				user_form.cleaned_data['hasło'])
			new_user.save()
			return render(request, 'account/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm
	return render(request, 'account/register.html', {'user_form': user_form})
