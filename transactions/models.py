from django.db import models
from accounts.models import AccountInfo

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(AccountInfo, on_delete=models.CASCADE, related_name='transactions')
    TRANSACTION_TYPE_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    transaction_amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.transaction_amount}"

class Transfer(models.Model):
    transfer_id = models.AutoField(primary_key=True)
    transfer_from_account = models.ForeignKey(AccountInfo, on_delete=models.CASCADE, related_name='transfers_from')
    transfer_to_account = models.ForeignKey(AccountInfo, on_delete=models.CASCADE, related_name='transfers_to')
    transfer_amount = models.DecimalField(max_digits=15, decimal_places=2)  # Daily limit of 100,000
    transfer_time = models.DateTimeField(auto_now_add=True)  # Reference to Transaction.transaction_time

    def __str__(self):
        return f"Transfer from {self.transfer_from_account} to {self.transfer_to_account} - {self.transfer_amount}"

    # 每日非約定轉帳最高限額為10 萬，約定轉帳最高限額為300 萬
    