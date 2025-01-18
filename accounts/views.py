from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages 
from django.utils.timezone import now

from .models import AccountInfo, SessionSettings
from .forms import RegistrationForm, EditProfileForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AccountInfo, SessionSettings

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AccountInfo, SessionSettings

def home(request):
	# 驗證是否已登入
	if not request.user.is_authenticated:
		return redirect('login')

	if request.method == "GET":
	
		account_info = AccountInfo.objects.get(account_user=request.user)
		account_no = account_info.account_No
		account_balance = account_info.account_balance

		# 獲取計時器設定
		session_setting, created = SessionSettings.objects.get_or_create(id=1)  ## 
		if session_setting:
			timeout_minutes = session_setting.timeout_minutes
		else: 
			timeout_minutes = 5
		print(f'GET..timeout: {timeout_minutes}')

		context = {
			'username': request.user.username,
			'account_no': account_no,
			'account_balance': account_balance,
			'timeout_minutes': timeout_minutes,
		}
		return render(request, 'common/home.html', context)

	# 處理計時器更新
	if request.method == "POST":
		timeout = int(request.POST.get("timeout_minutes", 5))
		print(f'POST...timeout: {timeout_minutes}')
		session_setting, created = SessionSettings.objects.get_or_create(id=1)
		session_setting.timeout_minutes = timeout
		session_setting.save()
		return redirect('home')

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

def set_session_timeout(request):
    if request.method == "POST":
        timeout = int(request.POST.get("timeout_minutes", 5))
        session_setting, created = SessionSettings.objects.get_or_create(id=1)
        session_setting.timeout_minutes = timeout
        session_setting.save()
        return redirect('home')
    
    session_setting = SessionSettings.objects.first()
    timeout_minutes = session_setting.timeout_minutes if session_setting else 5
    return render(request, 'common/set_session_timeout.html', {'timeout_minutes': timeout_minutes})

def reset_timer(request):
	# 獲取超時設置
	session_setting = SessionSettings.objects.first()
	timeout_minutes = session_setting.timeout_minutes if session_setting else 5  # 默認 90 分鐘

	# 重設 session timeout
	timeout_seconds = timeout_minutes * 60
	request.session.set_expiry(timeout_seconds)
	request.session['last_interaction'] = now().timestamp()

	return redirect('home')
