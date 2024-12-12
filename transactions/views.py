from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.db import transaction

from .forms import TransactionForm, TransferForm
from .models import AccountInfo, Transaction

def deposit(request):
    deposit_title = "Deposit Money to Account."
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            account = get_object_or_404(AccountInfo, account_user=request.user)
            deposit_amount = transaction_form.cleaned_data['transaction_amount']

            # Update account balance
            with transaction.atomic():
                account.account_balance += deposit_amount
                account.save()

                # Create a transaction record
                Transaction.objects.create(
                    account=account,
                    transaction_type='Deposit',
                    transaction_amount=deposit_amount
                )
            messages.success(request, 'Deposit successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Errors! Please correct the errors below.')
    else:
        transaction_form = TransactionForm()

    context = {'title': deposit_title, 'transaction_form': transaction_form  }
    return render(request, 'transactions/transactions_action.html', context)

def withdrawal(request):
    withdraw_title = "Withdrawal Money from Account."
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            account_info = get_object_or_404(AccountInfo, account_user=request.user)
            withdrawal_amount = transaction_form.cleaned_data['transaction_amount']

            # Check if the account has enough balance
            if account_info.account_balance >= withdrawal_amount:
                # Update account balance
                with transaction.atomic():
                    account_info.account_balance -= withdrawal_amount
                    account_info.save()

                    # Create a transaction record
                    Transaction.objects.create(
                        account=account_info,
                        transaction_type='Withdrawal',
                        transaction_amount=withdrawal_amount
                    )

                messages.success(request, 'Withdrawal successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Insufficient funds for this withdrawal.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        transaction_form = TransactionForm()

    context = {'title': withdraw_title, 'transaction_form': transaction_form}
    return render(request, 'transactions/transactions_action.html', context)

def transaction_report(request):
    report_title = "Transaction Report"
    transactions = Transaction.objects.filter(account__account_user=request.user)
    context = {'title':report_title, 'transactions': transactions}
    return render(request, 'transactions/transactions_report.html', context)

def transfer(request):
    pass


