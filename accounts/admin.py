from django.contrib import admin
from .models import User, UserAddress, AccountInfo

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'mobile',
                    'is_staff', 'is_active', 'date_joined', 'last_login']

admin.site.register(User, UserAdmin)

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'city', 'street_address', 'postal_code'] 

admin.site.register(UserAddress, UserAddressAdmin)

class AccountInfoAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'account_user', 'account_type', 'account_No', 'account_balance']

admin.site.register(AccountInfo, AccountInfoAdmin)

