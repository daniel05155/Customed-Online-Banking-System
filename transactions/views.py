from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.exceptions import ValidationError
from django.db import transaction

from .forms import TransactionForm, TransferForm
from .models import AccountInfo, Transaction, Transfer

from decimal import Decimal 
from .models import AccountInfo, Transaction, Transfer

from decimal import Decimal 

@login_required
def deposit(request):
    deposit_title = "Deposit Money to Account."
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            account = AccountInfo.objects.get(account_user=request.user)
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

    transaction_form = TransactionForm()
    context = {'title': deposit_title, 'transaction_form': transaction_form}
    return render(request, 'transactions/transactions_action.html', context)

@login_required
def withdrawal(request):
    withdraw_title = "Withdrawal Money from Account."
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            account_info = AccountInfo.objects.get(account_user=request.user)
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
        
    transaction_form = TransactionForm()
    context = {'title': withdraw_title, 'transaction_form': transaction_form}
    return render(request, 'transactions/transactions_action.html', context)

@login_required
def transaction_report(request):
    try:
        account_info = AccountInfo.objects.get(account_user=request.user)
        transactions = Transaction.objects.filter(transaction_account_info=account_info)
        context = {
            'username': request.user.username,
            'account_no': account_info.account_No,
            'transactions': transactions
        }
    except AccountInfo.DoesNotExist:
        context = {
            'username': request.user.username,
            'account_no': 'N/A',
            'transactions': [],
        }
    return render(request, 'transactions/transactions_report.html', context)

@login_required
def transfer(request):
    """
    1. 使用 transaction.atomic()。
    2. 為 from_account和to_account建立Transaction 記錄 (transaction_type='Transfer')。
    3. 連結該 Transaction 和 Transfer 。
    4. 檢查每日限額。
    5. 若成功則將 transfer_status 設為 'Completed'，並儲存 to_account 的餘額變動。
    """
    if request.method == 'POST':
        from_account_no = request.POST.get('from_account', '').strip()
        to_account_no   = request.POST.get('to_account', '').strip()
        amount_str      = request.POST.get('amount', '').strip()

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

        # 驗證金額
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Enter a valid amount greater than 0.')
            return redirect('transfer')
        
        # Ensure sufficient balance
        if from_account.account_balance < amount:
            messages.error(request, 'Insufficient balance in the sender account.')
            return redirect('transfer')

        # 使用 transaction.atomic()
        try:
            with transaction.atomic():
                # 1) 先扣款 (from_account)
                from_account.account_balance -= amount
                from_account.save()

                # 2) 建立 Transaction (type=Transfer)，並紀錄交易後餘額
                transfer_transaction = Transaction.objects.create(
                    transaction_account_info   = from_account,
                    transaction_type           = 'Transfer',
                    transaction_amount         = amount,
                    transaction_balance_after  = from_account.account_balance
                )

                # 3) 建立 Transfer object，將該 Transaction 與 from/to 帳戶關聯
                transfer_obj = Transfer.objects.create(
                    transfer_from_account  = from_account,
                    transfer_to_account    = to_account,
                    transfer_info          = transfer_transaction,
                    transfer_status        = 'Failed'  # 預設 Failed，檢查通過再改為 Completed
                )

                # 4) 檢查每日限額
                if transfer_obj.is_daily_limit_exceeded():
                    raise ValidationError("Daily limit exceeded.")

                # 5) 如果沒超過限額，才進行加款(to_account)，並將 status 改為 Completed
                to_account.account_balance += amount
                to_account.save()

                # 6) 建立to_account的Transaction (ype=Transfer)，並紀錄交易後餘額
                transfer_transaction = Transaction.objects.create(
                    transaction_account_info   = to_account,
                    transaction_type           = 'Transfer',
                    transaction_amount         = amount,
                    transaction_balance_after  = to_account.account_balance
                )

                transfer_obj.transfer_status = 'Completed'
                transfer_obj.save()

            messages.success(
                request,
                f'Successfully transferred {amount} from account {from_account_no} to account {to_account_no}.'
            )
        except ValidationError as e:
            # 若發生 ValidationError（例如超過每日限額），atomic 會回滾
            messages.error(request, str(e))

        return redirect('transfer')

    # Render the transfer form for GET request
    return render(request, 'transactions/transfer.html')
