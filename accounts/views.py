from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages 

from .models import AccountInfo
from .forms import RegistrationForm, EditProfileForm

def home(request): 
	if not request.user.is_authenticated:
		return redirect('login')
	try:
		account_info = AccountInfo.objects.get(account_user=request.user)
		account_no = account_info.account_No
	except AccountInfo.DoesNotExist:
		account_no='N/A'
	
	context = {
		'username': request.user.username,
		'account_no': account_no
	}
	return render(request, 'common/home.html', context)

def login_user (request):
	if request.method == 'POST': 			# if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:				# if user exist
			login(request, user)
			return redirect('home') 		# routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login')  	    # == return render(request, 'accounts/login.html', {})	
	else:
		return render(request, 'accounts/login.html', {})

def logout_user(request):
	logout(request)
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
				messages.success(request,('You are registered successfully!'))	
				login(request, user)
				return redirect('home')
			else:
				messages.error(request, 'Please correct the errors below.')
		else:
			messages.error(request, 'Registration form is not valid.')
	return render(request, 'accounts/register.html', context)

# Error
def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('home')
		else:
			return redirect('edit_profile')
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
			return redirect('home')
	# Passes in user information 
	form = PasswordChangeForm(user= request.user)
	context = {'form': form}
	return render(request, 'accounts/change_password.html', context)
