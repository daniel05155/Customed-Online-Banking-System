from django.contrib import admin
from .models import Transaction, Transfer

class Transaction_Inline(admin.TabularInline):
    '''
    Foreign Key: Transaction.transaction_account_info-> AccountInfo
    '''
    model = Transaction

class TransactionAdmin(admin.ModelAdmin):
    '''
    Register Transaction models.
    '''
    list_display = ('transaction_id',  'transaction_account_info', 'transaction_type', 'transaction_time' , 'transaction_amount', 'transaction_note')
    list_filter = ('transaction_amount', 'transaction_time')
    search_fields = ('transaction_id', 'transaction_type', 'transaction_time', 'transaction_amount', 'transaction_note')
    inlunes = [Transaction_Inline]

admin.site.register(Transaction, TransactionAdmin)

class Transfer_Inline(admin.TabularInline):
    '''
    Foreign Key: Transfer.transfer_info-> Transaction etc
    '''
    model = Transfer    

class TransferAdmin(admin.ModelAdmin):
    '''
    Register Transfer models.
    '''
    list_display = ('transfer_id', 'transfer_from_account', 'transfer_to_account', 'transfer_info', 'transfer_status')
    search_fields = ('transfer_id', 'transfer_from_account', 'transfer_to_account', 'transfer_info', 'transfer_status')

admin.site.register(Transfer, TransferAdmin)
