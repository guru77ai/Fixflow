"""
Admin configuration for Accounting module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    AccountType, AccountCategory, ChartOfAccounts, Account,
    JournalEntry, JournalEntryLine, Ledger, BankAccount,
    BankTransaction, TrialBalance, FinancialStatement
)


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'normal_balance', 'description')
    list_filter = ('normal_balance',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(AccountCategory)
class AccountCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'account_type', 'parent', 'is_active')
    list_filter = ('account_type', 'parent', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')


@admin.register(ChartOfAccounts)
class ChartOfAccountsAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'is_active', 'is_default')
    list_filter = ('is_active', 'is_default', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'account_type', 'category', 'current_balance', 'status')
    list_filter = ('account_type', 'category', 'status', 'is_bank', 'is_cash', 'organization', 'branch')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('code', 'name', 'description')
        }),
        (_('Classification'), {
            'fields': ('chart_of_accounts', 'account_type', 'category', 'parent')
        }),
        (_('Account Type Flags'), {
            'fields': ('is_bank', 'is_cash', 'is_revenue', 'is_expense', 'is_asset', 'is_liability', 'is_equity')
        }),
        (_('Balances'), {
            'fields': ('opening_balance', 'current_balance')
        }),
        (_('Settings'), {
            'fields': ('status', 'allow_reconciliation')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('chart_of_accounts', 'account_type', 'category', 'parent', 'organization', 'branch')


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('entry_number', 'reference', 'description', 'entry_date', 'is_posted', 'created_at')
    list_filter = ('is_posted', 'entry_date', 'organization', 'branch')
    search_fields = ('entry_number', 'reference', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('entry_number', 'reference', 'description', 'entry_date')
        }),
        (_('Status'), {
            'fields': ('is_posted', 'posted_at', 'created_by', 'approved_by')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('created_by', 'approved_by', 'organization', 'branch')


@admin.register(JournalEntryLine)
class JournalEntryLineAdmin(admin.ModelAdmin):
    list_display = ('journal_entry', 'account', 'description', 'debit', 'credit')
    list_filter = ('journal_entry', 'account')
    readonly_fields = ('uuid',)
    raw_id_fields = ('journal_entry', 'account')


@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('account', 'entry_date', 'reference', 'description', 'debit', 'credit', 'balance')
    list_filter = ('account', 'entry_date', 'created_by', 'organization', 'branch')
    search_fields = ('account__code', 'account__name', 'reference', 'description')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('account', 'created_by', 'organization', 'branch')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account', 'bank_name', 'account_number', 'account_holder', 'current_balance')
    list_filter = ('bank_name', 'organization', 'branch')
    search_fields = ('bank_name', 'account_number', 'account_holder')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('account', 'organization', 'branch')


@admin.register(BankTransaction)
class BankTransactionAdmin(admin.ModelAdmin):
    list_display = ('bank_account', 'transaction_type', 'transaction_number', 'amount', 'transaction_date', 'is_reconciled')
    list_filter = ('bank_account', 'transaction_type', 'transaction_date', 'is_reconciled', 'organization', 'branch')
    search_fields = ('transaction_number', 'reference', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('bank_account', 'transaction_type', 'transaction_number', 'reference')
        }),
        (_('Details'), {
            'fields': ('description', 'amount', 'fee', 'net_amount', 'transaction_date')
        }),
        (_('Reconciliation'), {
            'fields': ('is_reconciled', 'reconciled_at', 'reconciled_by')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('bank_account', 'reconciled_by', 'organization', 'branch')


@admin.register(TrialBalance)
class TrialBalanceAdmin(admin.ModelAdmin):
    list_display = ('period_start', 'period_end', 'account', 'debit', 'credit')
    list_filter = ('period_start', 'period_end', 'account', 'organization', 'branch')
    readonly_fields = ('uuid',)
    raw_id_fields = ('account', 'organization', 'branch')


@admin.register(FinancialStatement)
class FinancialStatementAdmin(admin.ModelAdmin):
    list_display = ('name', 'statement_type', 'period_start', 'period_end', 'generated_by')
    list_filter = ('statement_type', 'period_start', 'period_end', 'generated_by', 'organization', 'branch')
    search_fields = ('name', 'statement_type')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('generated_by', 'organization', 'branch')
