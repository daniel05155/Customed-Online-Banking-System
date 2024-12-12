from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, UserAddress, AccountInfo

# https://stackoverflow.com/questions/2303268/djangos-forms-form-vs-forms-modelform
import random
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile, UserAddress, AccountInfo

# https://stackoverflow.com/questions/2303268/djangos-forms-form-vs-forms-modelform
class RegistrationForm(UserCreationForm):
    # Adding fields from UserAddress and AccountInfo
    country = forms.CharField(max_length=255, label="Country")
    city    = forms.CharField(max_length=255, label="City")
    street_address = forms.CharField(max_length=255, label="Street Address")
    postal_code = forms.CharField(max_length=20, label="Postal Code")
    account_type = forms.ChoiceField(choices=AccountInfo.ACCOUNT_TYPE_CHOICES, label="Account Type")

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'username', 'password1', 'password2',
            'email', 'mobile', 'gender', 'birth_date', 
            'country', 'city', 'street_address', 'postal_code', 'account_type'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def generate_unique_account_no(self):
        while True:
            account_no = str(random.randint(10000000001, 99999999999))
            if not AccountInfo.objects.filter(account_No=account_no).exists():
                return account_no

    def save(self, commit=True):
        # Save the UserProfile instance
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create the UserAddress instance
            UserAddress.objects.create(
                user=user,
                country=self.cleaned_data['country'],
                city=self.cleaned_data['city'],
                street_address=self.cleaned_data['street_address'],
                postal_code=self.cleaned_data['postal_code']
            )

            # Create the AccountInfo instance
            account_no = self.generate_unique_account_no()
            AccountInfo.objects.create(
                account_user=user,
                account_type=self.cleaned_data['account_type'],
                account_No=account_no
            )
        return user
    
class LoginForm(forms.ModelForm):
    username = forms.CharField(label='使用者名稱')
    password = forms.CharField(widget=forms.PasswordInput(), label='密碼')
    class Meta:
        model = UserProfile
        fields = ['username', 'password']

class EditProfileForm(UserChangeForm):
	
	password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = UserProfile
		#excludes private information from User
		fields = ('username', 'first_name', 'last_name', 'email','password',)
	