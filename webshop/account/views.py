from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from shop.tokens import account_activation_token
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
	return render(request, 'registration/login.html', {'form': form})


def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			birthday = user_form.validate_birthday()
			if birthday != "01-01-0001":
				new_user = user_form.save(commit=False)
				new_user.set_password(
					user_form.cleaned_data['hasło'])
				new_user.is_active = False
				new_user.save()
				update_profile(request, new_user, birthday)
				current_site = 'localhost:8000'
				mail_subject = 'Aktywuj konto'
				message = render_to_string('account/acc_active_email.html',
										   {'user': new_user,
											'domain': current_site,
											'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
											'token': account_activation_token.make_token(new_user),
											})
				to_email = user_form.cleaned_data.get('email')
				email = EmailMessage(mail_subject, message, to=[to_email])
				email.send()
				#HttpResponse('Powierdź swojego maila, aby dokończyć rejestrację')
				return render(request, 'account/confirm_mail.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm
	return render(request, 'account/register.html', {'user_form': user_form})


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		# return redirect('home')
		return render(request, 'account/register_done.html', {'new_user': user})
	else:
		return render(request, 'account/link_invalid.html')


def user_logout(request):
	logout(request)
	return HttpResponse('Wylogowano pomyślnie')


def update_profile(request, user_id, birthday):
	user = user_id
	user.profile.birthday = birthday
	user.save()
