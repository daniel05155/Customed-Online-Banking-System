import random
from django.db import models

# 批量創建用戶
class AccountManager(models.Manager):
    def create_account(self, account_user, account_type, initial_balance=0.00):
        # Generate a unique account_No
        while True:
            account_no = str(random.randint(10000000001, 99999999999))  # 11-digit random number
            if not self.filter(account_No=account_no).exists():
                break
        
        # Create and return the account
        account = self.create(
            account_user=account_user,
            account_type=account_type,
            account_No=account_no,
            account_balance=initial_balance
        )
        return account
