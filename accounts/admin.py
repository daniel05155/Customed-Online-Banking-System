from django.contrib import admin
from .models import UserInfo, UserAddress, AccountInfo, SessionSettings

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'mobile',
                    'is_staff', 'is_active', 'date_joined', 'last_login']

admin.site.register(UserInfo, UserAdmin)

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'city', 'street_address', 'postal_code'] 

admin.site.register(UserAddress, UserAddressAdmin)

class AccountInfoAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'account_user', 'account_type', 'account_No', 'account_balance']

admin.site.register(AccountInfo, AccountInfoAdmin)

class SessionSettingsAdmin(admin.ModelAdmin):
    list_display = ['timeout_minutes', 'updated_at']

admin.site.register(SessionSettings, SessionSettingsAdmin)
