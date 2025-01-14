# https://stackoverflow.com/questions/2303268/djangos-forms-form-vs-forms-modelform
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import UserInfo, UserAddress, AccountInfo

class RegistrationForm(UserCreationForm):
    
    # Adding fields from UserAddress and AccountInfo
    country = forms.CharField(max_length=255, label="Country")
    city    = forms.CharField(max_length=255, label="City")
    street_address = forms.CharField(max_length=255, label="Street Address")
    postal_code = forms.CharField(max_length=20, label="Postal Code")
    account_type = forms.ChoiceField(choices=AccountInfo.ACCOUNT_TYPE_CHOICES, label="Account Type")
    class Meta:
        model = UserInfo
        fields = [
            'username', 'password1', 'password2','first_name', 'last_name',
            'email', 'mobile', 'gender', 'birth_date', 
            'country', 'city', 'street_address', 'postal_code', 'account_type'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        '''
        Save the UserProfile instance
        '''
        user = super().save(commit=False)
        if commit:
            user.save()
            UserAddress.objects.create(
                user=user,
                country=self.cleaned_data['country'],
                city=self.cleaned_data['city'],
                street_address=self.cleaned_data['street_address'],
                postal_code=self.cleaned_data['postal_code']
            )

            # Create AccountInfo instance
            AccountInfo.objects.create_account(
                account_user=user,
                account_type=self.cleaned_data['account_type'],
                initial_balance=0.00  # Default initial balance
            )
        return user
    
class LoginForm(forms.ModelForm):
    username = forms.CharField(label='使用者名稱')
    password = forms.CharField(widget=forms.PasswordInput(), label='密碼')
    class Meta:
        model = UserInfo
        fields = ['username', 'password']

class EditProfileForm(UserChangeForm):
	
	password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = UserInfo
		#excludes private information from User
		fields = ('username', 'first_name', 'last_name', 'email','password',)
	