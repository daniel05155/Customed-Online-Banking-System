from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 

from .forms import RegistrationForm, EditProfileForm

def home(request): 
	if request.method=='POST':
		return render(request, 'accounts/home.html', {})
	return render(request, 'accounts/home.html', {})

def login_user (request):
	if request.method == 'POST': 			# if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:				# if user exist
			login(request, user)
			messages.success(request,('You are logged in'))
			return redirect('home') 		# routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login')  	    # == return render(request, 'accounts/login.html', {})	
	else:
		return render(request, 'accounts/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('You are now logged out'))
	return redirect('home')

def register_user(request):
	registration_form  = RegistrationForm() 
	context = {'registration_form': registration_form }
	if request.method =='POST':
		registration_form  = RegistrationForm(request.POST)
		if registration_form.is_valid():
			registration_form.save()
			username = registration_form.cleaned_data['username']
			password = registration_form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request,user)
				messages.success(request, ('You have already registered!'))
				return redirect('home')
			else:
				messages.error(request, 'Please correct the errors below.')
	# GET 
	return render(request, 'accounts/register.html', context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
		else:
			messages.success(request, ('Review the form'))
			return redirect('edit_profile')
	else:
		form = EditProfileForm(instance=request.user)  	# Passes in user information 
		context = {'form': form}
		return render(request, 'accounts/edit_profile.html', context)

# https://docs.djangoproject.com/en/5.1/topics/auth/default/
def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	# Passes in user information 
	form = PasswordChangeForm(user= request.user)
	context = {'form': form}
	return render(request, 'accounts/change_password.html', context)
