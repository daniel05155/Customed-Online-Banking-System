from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.db import transaction

from .forms import TransactionForm, TransferForm
from .models import AccountInfo, Transaction, Transfer

from decimal import Decimal 

def deposit(request):
    deposit_title = "Deposit Money to Account."
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            account = AccountInfo.objects.get(account_user=request.user)
            deposit_amount = transaction_form.cleaned_data['transaction_amount']

            # Update account balance
            with transaction.atomic():
                account.account_balance += deposit_amount
                account.save()

                # Create a transaction record
                Transaction.objects.create(
                    transaction_account_info = account,
                    transaction_type = 'Deposit',
                    transaction_amount = deposit_amount
                )
            messages.success(request, 'Deposit successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Errors! Please correct the errors below.')

    transaction_form = TransactionForm()
    context = {'title': deposit_title, 'transaction_form': transaction_form}
    return render(request, 'transactions/transactions_action.html', context)

def withdrawal(request):
    withdraw_title = "Withdrawal Money from Account."
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            account_info = AccountInfo.objects.get(account_user=request.user)
            withdrawal_amount = transaction_form.cleaned_data['transaction_amount']

            # Check if the account has enough balance
            if account_info.account_balance >= withdrawal_amount:
                
                # Update account balance
                with transaction.atomic():
                    account_info.account_balance -= withdrawal_amount
                    account_info.save()

                    # Create a transaction record
                    Transaction.objects.create(
                        transaction_account_info = account_info,
                        transaction_type   = 'Withdrawal',
                        transaction_amount = withdrawal_amount
                    )

                messages.success(request, 'Withdrawal successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Insufficient funds for this withdrawal.')
        else:
            messages.error(request, 'Please correct the errors below.')
        
    transaction_form = TransactionForm()
    context = {'title': withdraw_title, 'transaction_form': transaction_form}
    return render(request, 'transactions/transactions_action.html', context)

@login_required
def transaction_report(request):
    account_info = AccountInfo.objects.filter(account_user=request.user).first()
    transactions = []
    if account_info:
        transactions = Transaction.objects.filter(transaction_account_info=account_info)
    context = {'transactions': transactions}
    return render(request, 'transactions/transactions_report.html', context)

@login_required
def transfer(request):
    if request.method == 'POST':
        from_account_no = request.POST.get('from_account', '').strip()
        to_account_no = request.POST.get('to_account', '').strip()
        amount_str = request.POST.get('amount', '').strip()

        # Validate input fields
        if not from_account_no or not to_account_no or not amount_str:
            messages.error(request, 'All fields are required.')
            return redirect('transfer')

        try:
            # Retrieve sender's account
            from_account = AccountInfo.objects.get(account_No=from_account_no)
        except AccountInfo.DoesNotExist:
            messages.error(request, f'Sender account {from_account_no} does not exist.')
            return redirect('transfer')

        try:
            # Retrieve receiver's account
            to_account = AccountInfo.objects.get(account_No=to_account_no)
        except AccountInfo.DoesNotExist:
            messages.error(request, f'Recipient account {to_account_no} does not exist.')
            return redirect('transfer')

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Enter a valid amount greater than 0.')
            return redirect('transfer')
        
        # Ensure sufficient balance
        if from_account.account_balance < amount:
            messages.error(request, 'Insufficient balance in the sender account.')
            return redirect('transfer')

        # Perform the transfer
        from_account.account_balance =  from_account.account_balance - Decimal(amount)
        to_account.account_balance = to_account.account_balance + Decimal(amount)
 
        # Save changes to the database
        from_account.save()
        to_account.save()

        messages.success(request, f'Successfully transferred {amount} from account {from_account_no} to account {to_account_no}.')
        return redirect('transfer')

    # Render the transfer form for GET request
    return render(request, 'transactions/transfer.html')

