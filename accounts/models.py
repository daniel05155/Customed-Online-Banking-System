from django.db import models
from django.contrib.auth.models import AbstractUser

# https://docs.djangoproject.com/en/5.1/ref/contrib/auth/
class UserProfile(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender      = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date  = models.DateField(null=True, blank=True)                 # Format: YYYY-MM-DD
    mobile      = models.CharField(max_length=10, null=True, blank=True)  # Must be 10 digits

    def __str__(self):
        return self.username

class UserAddress(models.Model):
    user_address_id = models.AutoField(primary_key=True)
    #  == models.ForeignKey(unique=True)
    user    = models.OneToOneField(UserProfile, on_delete=models.CASCADE) #
    country = models.CharField(max_length=255)
    city    = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.country}"

class AccountInfo(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Personal', 'Personal'),
        ('Business', 'Business'),
    ]
    account_id = models.AutoField(primary_key=True)
    account_user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=8, choices=ACCOUNT_TYPE_CHOICES)
    account_No = models.CharField(max_length=11, unique=True)       # Must be 11 digits (10000000001-99999999999)
    account_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.account_No} ({self.account_type})"