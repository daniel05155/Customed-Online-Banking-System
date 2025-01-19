from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from accounts.models import AccountInfo

class Transaction(models.Model):
    
    TRANSACTION_TYPE_CHOICES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer_Sender', 'Transfer_Sender'),
        ('Transfer_Receiver', 'Transfer_Receiver'),
    ]
    transaction_id      = models.AutoField(primary_key=True)
    transaction_account_info = models.ForeignKey(AccountInfo, on_delete=models.CASCADE, related_name='transactions')  # One-to-Many
    transaction_type    = models.CharField(max_length=30, choices=TRANSACTION_TYPE_CHOICES)
    transaction_time    = models.DateTimeField(auto_now_add=True)
    transaction_amount  = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_note    = models.TextField(null=True, blank=True, default="")                    # transaction remarks
    transaction_balance_after = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # Balance after each transaction
class Transfer(models.Model):
    
    # 每筆轉帳的處理狀態
    TRANSFER_STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    transfer_id             = models.AutoField(primary_key=True)
    transfer_from_account   = models.ForeignKey(AccountInfo, on_delete=models.CASCADE, related_name='transfers_from')
    transfer_to_account     = models.ForeignKey(AccountInfo, on_delete=models.CASCADE, related_name='transfers_to')
    transfer_info           = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='transfers',null=True, blank=True)  # Link to Transaction
    transfer_status         = models.CharField(max_length=10, choices=TRANSFER_STATUS_CHOICES, default='Failed')
    # transfer_amount   = models.DecimalField(max_digits=15, decimal_places=2)      # FK: Daily limit of 100,000
    # transfer_time     = models.DateTimeField(auto_now_add=True)                   # FK: Transaction.transaction_time
    
    def clean(self):
        # 確保來源和目標帳戶不能相同
        if self.transfer_from_account == self.transfer_to_account:
            raise ValidationError("Transfer from and to accounts cannot be the same.")
        # 限制金額必須為正值
        if self.transfer_amount <= 0:
            raise ValidationError("Transfer amount must be greater than zero.")
    
    def is_daily_limit_exceeded(self):
        today = now().date()
        daily_transfers = Transfer.objects.filter(
            transfer_from_account=self.transfer_from_account,
            transfer_info__transaction_time__date=today
        ).select_related('transfer_info')  # 預加載 transfer_info 關聯數據

        total_amount = daily_transfers.aggregate(
            total_amount=models.Sum('transfer_info__transaction_amount')
        )['total_amount'] or 0  # 如果無結果，設為 0

        # 包含當前交易金額計算日額
        return total_amount + (self.transfer_info.transaction_amount if self.transfer_info else 0) > 100000

