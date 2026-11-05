"""
Accounting Models for FixSoftRepair Pro
Accounting module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel, CurrencyField


class AccountType(UUIDModel, TimeStampedModel):
    """Account type (Asset, Liability, Equity, Revenue, Expense)"""
    name = models.CharField(_('Name'), max_length=50, unique=True)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    normal_balance = models.CharField(_('Normal Balance'), max_length=10, choices=[('debit', 'Debit'), ('credit', 'Credit')], default='debit')
    description = models.TextField(_('Description'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Account Type')
        verbose_name_plural = _('Account Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class AccountCategory(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Account category"""
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name='categories', verbose_name=_('Account Type'))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_('Parent Category'))
    description = models.TextField(_('Description'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Account Category')
        verbose_name_plural = _('Account Categories')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name


class ChartOfAccounts(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Chart of accounts"""
    name = models.CharField(_('Name'), max_length=200)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_default = models.BooleanField(_('Default'), default=False)
    
    class Meta:
        verbose_name = _('Chart of Accounts')
        verbose_name_plural = _('Chart of Accounts')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name


class Account(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """General ledger account"""
    ACCOUNT_STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('frozen', _('Frozen')),
    ]
    
    chart_of_accounts = models.ForeignKey(ChartOfAccounts, on_delete=models.PROTECT, related_name='accounts', verbose_name=_('Chart of Accounts'))
    account_type = models.ForeignKey(AccountType, on_delete=models.PROTECT, related_name='accounts', verbose_name=_('Account Type'))
    category = models.ForeignKey(AccountCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='accounts', verbose_name=_('Category'))
    
    code = models.CharField(_('Code'), max_length=20, unique=True)
    name = models.CharField(_('Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True, null=True)
    
    status = models.CharField(_('Status'), max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='active')
    
    is_bank = models.BooleanField(_('Bank Account'), default=False)
    is_cash = models.BooleanField(_('Cash Account'), default=False)
    is_revenue = models.BooleanField(_('Revenue Account'), default=False)
    is_expense = models.BooleanField(_('Expense Account'), default=False)
    is_asset = models.BooleanField(_('Asset Account'), default=False)
    is_liability = models.BooleanField(_('Liability Account'), default=False)
    is_equity = models.BooleanField(_('Equity Account'), default=False)
    
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_('Parent Account'))
    
    opening_balance = CurrencyField(_('Opening Balance'), default=0.00)
    current_balance = CurrencyField(_('Current Balance'), default=0.00)
    
    allow_reconciliation = models.BooleanField(_('Allow Reconciliation'), default=False)
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
            models.Index(fields=['account_type']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def display_name(self):
        return f"{self.code} - {self.name}"


class JournalEntry(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Journal entry"""
    entry_number = models.CharField(_('Entry Number'), max_length=50, unique=True)
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    description = models.TextField(_('Description'))
    
    entry_date = models.DateField(_('Entry Date'))
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_journal_entries', verbose_name=_('Created By'))
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_journal_entries', verbose_name=_('Approved By'))
    
    is_posted = models.BooleanField(_('Posted'), default=False)
    posted_at = models.DateTimeField(_('Posted At'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Journal Entry')
        verbose_name_plural = _('Journal Entries')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entry_number']),
            models.Index(fields=['entry_date']),
        ]
    
    def __str__(self):
        return f"{self.entry_number} - {self.description}"


class JournalEntryLine(UUIDModel, TimeStampedModel):
    """Line items in a journal entry"""
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines', verbose_name=_('Journal Entry'))
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='journal_lines', verbose_name=_('Account'))
    
    description = models.TextField(_('Description'), blank=True, null=True)
    
    debit = CurrencyField(_('Debit'), default=0.00)
    credit = CurrencyField(_('Credit'), default=0.00)
    
    class Meta:
        verbose_name = _('Journal Entry Line')
        verbose_name_plural = _('Journal Entry Lines')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.journal_entry.entry_number} - {self.account.code}"


class Ledger(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """General ledger"""
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='ledger_entries', verbose_name=_('Account'))
    
    entry_date = models.DateField(_('Entry Date'))
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    description = models.TextField(_('Description'))
    
    debit = CurrencyField(_('Debit'), default=0.00)
    credit = CurrencyField(_('Credit'), default=0.00)
    balance = CurrencyField(_('Balance'), default=0.00)
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_ledger_entries', verbose_name=_('Created By'))
    
    class Meta:
        verbose_name = _('Ledger')
        verbose_name_plural = _('Ledger')
        ordering = ['-entry_date', 'created_at']
        indexes = [
            models.Index(fields=['account']),
            models.Index(fields=['entry_date']),
        ]
    
    def __str__(self):
        return f"{self.account.code} - {self.entry_date}"


class BankAccount(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Bank account"""
    account = models.OneToOneField(Account, on_delete=models.PROTECT, related_name='bank_account', verbose_name=_('Account'))
    
    bank_name = models.CharField(_('Bank Name'), max_length=200)
    branch_name = models.CharField(_('Branch Name'), max_length=200, blank=True, null=True)
    account_number = models.CharField(_('Account Number'), max_length=50)
    account_holder = models.CharField(_('Account Holder'), max_length=200)
    
    current_balance = CurrencyField(_('Current Balance'), default=0.00)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Bank Account')
        verbose_name_plural = _('Bank Accounts')
        ordering = ['bank_name']
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


class BankTransaction(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Bank transaction"""
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', _('Deposit')),
        ('withdrawal', _('Withdrawal')),
        ('transfer_in', _('Transfer In')),
        ('transfer_out', _('Transfer Out')),
        ('fee', _('Bank Fee')),
        ('interest', _('Interest')),
        ('other', _('Other')),
    ]
    
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name='transactions', verbose_name=_('Bank Account'))
    transaction_type = models.CharField(_('Transaction Type'), max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    
    transaction_number = models.CharField(_('Transaction Number'), max_length=100, blank=True, null=True)
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    description = models.TextField(_('Description'))
    
    amount = CurrencyField(_('Amount'), default=0.00)
    fee = CurrencyField(_('Fee'), default=0.00)
    net_amount = CurrencyField(_('Net Amount'), default=0.00)
    
    transaction_date = models.DateField(_('Transaction Date'))
    
    is_reconciled = models.BooleanField(_('Reconciled'), default=False)
    reconciled_at = models.DateTimeField(_('Reconciled At'), blank=True, null=True)
    reconciled_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reconciled_transactions', verbose_name=_('Reconciled By'))
    
    class Meta:
        verbose_name = _('Bank Transaction')
        verbose_name_plural = _('Bank Transactions')
        ordering = ['-transaction_date']
        indexes = [
            models.Index(fields=['bank_account']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['transaction_date']),
        ]
    
    def __str__(self):
        return f"{self.transaction_number} - {self.description}"


class TrialBalance(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Trial balance"""
    period_start = models.DateField(_('Period Start'))
    period_end = models.DateField(_('Period End'))
    
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='trial_balances', verbose_name=_('Account'))
    
    opening_debit = CurrencyField(_('Opening Debit'), default=0.00)
    opening_credit = CurrencyField(_('Opening Credit'), default=0.00)
    
    debit = CurrencyField(_('Debit'), default=0.00)
    credit = CurrencyField(_('Credit'), default=0.00)
    
    closing_debit = CurrencyField(_('Closing Debit'), default=0.00)
    closing_credit = CurrencyField(_('Closing Credit'), default=0.00)
    
    class Meta:
        verbose_name = _('Trial Balance')
        verbose_name_plural = _('Trial Balances')
        ordering = ['account__code']
        unique_together = [['organization', 'period_start', 'period_end', 'account']]
    
    def __str__(self):
        return f"{self.account.code} - {self.period_start} to {self.period_end}"


class FinancialStatement(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Financial statement"""
    STATEMENT_TYPE_CHOICES = [
        ('balance_sheet', _('Balance Sheet')),
        ('income_statement', _('Income Statement')),
        ('cash_flow', _('Cash Flow Statement')),
        ('equity', _('Statement of Equity')),
    ]
    
    name = models.CharField(_('Name'), max_length=200)
    statement_type = models.CharField(_('Statement Type'), max_length=20, choices=STATEMENT_TYPE_CHOICES)
    
    period_start = models.DateField(_('Period Start'))
    period_end = models.DateField(_('Period End'))
    
    data = models.JSONField(_('Data'), blank=True, null=True)
    
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_statements', verbose_name=_('Generated By'))
    
    class Meta:
        verbose_name = _('Financial Statement')
        verbose_name_plural = _('Financial Statements')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.period_start} to {self.period_end}"
