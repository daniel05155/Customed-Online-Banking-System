from django import forms
from .models import Transaction, Transfer

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_amount']       # Remove "transaction_type" to allow views.py to set it
        widgets = {
            # 'transaction_type': forms.Select(choices=Transaction.TRANSACTION_TYPE_CHOICES),
            'transaction_amount': forms.NumberInput(attrs={'step': '1'}),
        }

class TransferForm(TransactionForm):
    # from_account_id = forms.IntegerField()
    # to_account_id = forms.IntegerField()
    # transfer_amount = forms.DecimalField(max_digits=15, decimal_places=2)
    class Meta:
        model = Transfer
        fields = ['transfer_from_account', 'transfer_to_account', 'transfer_amount']
