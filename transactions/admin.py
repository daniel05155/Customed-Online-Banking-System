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

# class Transfer_Inline(admin.TabularInline):
#     '''
#     Foreign Key: Transfer.transfer_info-> Transaction etc
#     '''
#     model = Transfer    


class TransferAdmin(admin.ModelAdmin):
    '''
    Register Transfer models.
    '''
    list_display = (
        'transfer_id', 
        'get_transfer_from_account_no', 
        'get_transfer_to_account_no', 
        'transfer_info', 
        'transfer_status'
    )
    search_fields = (
        'transfer_id', 
        'transfer_from_account__account_No', 
        'transfer_to_account__account_No', 
        'transfer_info', 
        'transfer_status'
    )
    
    # 自定義欄位顯示 account_No
    @admin.display(description='From Account No')
    def get_transfer_from_account_no(self, obj):
        return obj.transfer_from_account.account_No

    @admin.display(description='To Account No')
    def get_transfer_to_account_no(self, obj):
        return obj.transfer_to_account.account_No

admin.site.register(Transfer, TransferAdmin)

