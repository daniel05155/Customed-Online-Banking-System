from django import forms
from .models import Transaction, Transfer

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_amount', 'transaction_note']       # Remove "transaction_type" to allow views.py to set it
        widgets = {
            'transaction_amount': forms.NumberInput(attrs={'step': '1'}),
        }
        
class TransferForm(TransactionForm):

    class Meta:
        model = Transfer
        fields = ['transfer_from_account', 'transfer_to_account']
