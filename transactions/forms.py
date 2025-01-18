from django import forms
from .models import Transaction, Transfer

import datetime
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

class TransactionDateRangeForm(forms.Form):
    daterange = forms.CharField(required=False)
    
    def clean_daterange(self):
        daterange = self.cleaned_data.get("daterange")
        if not daterange:
            raise forms.ValidationError("Date range is required.")
        try:
            start_date, end_date = daterange.split(' - ')
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
            return [start_date, end_date]
        except (ValueError, AttributeError):
            raise forms.ValidationError("Invalid date range format. Expected 'YYYY-MM-DD - YYYY-MM-DD'.")

