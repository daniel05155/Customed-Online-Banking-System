from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import AccountManager

# https://docs.djangoproject.com/en/5.1/ref/contrib/auth/
class UserInfo(AbstractUser):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    username    = models.CharField(max_length=50, unique=True, blank=False, null=False, default="")
    gender      = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date  = models.DateField(null=True, blank=True)                 # Format: YYYY-MM-DD
    mobile      = models.CharField(max_length=10, null=True, blank=True)  # Must be 10 digits

    USERNAME_FIELD = 'username'  # Override the default username field
    REQUIRED_FIELDS = []         # Additional required fields
    
class UserAddress(models.Model):
    
    user_address_id = models.AutoField(primary_key=True)
    user    = models.OneToOneField(UserInfo, on_delete=models.CASCADE)   ##  == models.ForeignKey(unique=True)
    country = models.CharField(max_length=255)
    city    = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

class AccountInfo(models.Model):
    
    ACCOUNT_TYPE_CHOICES = [
        ('Personal', 'Personal'),
        ('Business', 'Business'),
    ]
    account_id   = models.AutoField(primary_key=True)
    account_user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)             # User Can have only one accounts
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE_CHOICES)
    account_No   = models.CharField(max_length=11, unique=True)                         # Must be 11 digits (10000000001-99999999999)
    account_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Decimal field
    
    # Bind the custom manager
    objects = AccountManager()

