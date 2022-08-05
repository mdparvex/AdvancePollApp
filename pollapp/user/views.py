from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect

from django.urls import reverse

# Create your views here.

def Register(request):
	if request.method == 'POST':
		check1 = False
		check2 = False
		check3 = False

		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password1 = form.cleaned_data['password1']
			password2 = form.cleaned_data['password2']
			email = form.cleaned_data['email']

			if password1 != password2:
				check1 = True
			if User.objects.filter(username=username).exists():
				check2 = True
			if User.objects.filter(email=email).exists():
				check3 = True

			if check1 or check2 or check3:
				messages.error(request, "Registration Falied", extra_tags= 'alert alert-warning alert-dismissible fade show')
				return redirect('register')
			else:
				user = User.objects.create_user(username=username, password=password1, email=email)
				messages.success(request, f"Registration Sucessfull{user.username}",extra_tags='alert alert-success alert-dismissible fade show')
				return redirect('login')

	else:
		user = UserRegistrationForm()
	return render(request, 'user/register.html',{"form":user})

def Login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			#changed
			return HttpResponseRedirect(reverse('index'))
			
		else:
			messages.error(request, "Username Or Password is incorrect!",
							extra_tags='alert alert-warning alert-dismissible fade show')

	return render(request, 'user/login.html')

def Logout(request):
	logout(request)
	return redirect('login')
