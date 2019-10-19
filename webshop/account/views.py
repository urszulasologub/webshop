from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])
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

