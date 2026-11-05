"""
Serializers for Accounting module
"""
from rest_framework import serializers
from .models import (
    AccountType, AccountCategory, ChartOfAccounts, Account,
    JournalEntry, JournalEntryLine, Ledger, BankAccount,
    BankTransaction, TrialBalance, FinancialStatement
)


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'


class AccountCategorySerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer(read_only=True)
    account_type_id = serializers.UUIDField(source='account_type.uuid', write_only=True)
    parent = serializers.StringField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = AccountCategory
        fields = '__all__'


class ChartOfAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartOfAccounts
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer(read_only=True)
    account_type_id = serializers.UUIDField(source='account_type.uuid', write_only=True)
    category = AccountCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    chart_of_accounts = ChartOfAccountsSerializer(read_only=True)
    chart_of_accounts_id = serializers.UUIDField(source='chart_of_accounts.uuid', write_only=True, required=False)
    parent = serializers.StringField(source='parent.code', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'current_balance')


class JournalEntrySerializer(serializers.ModelSerializer):
    created_by = serializers.StringField(source='created_by.get_full_name', read_only=True)
    created_by_id = serializers.UUIDField(source='created_by.uuid', write_only=True, required=False)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = JournalEntry
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'entry_number', 'posted_at')


class JournalEntryLineSerializer(serializers.ModelSerializer):
    journal_entry = serializers.StringField(source='journal_entry.entry_number', read_only=True)
    journal_entry_id = serializers.UUIDField(source='journal_entry.uuid', write_only=True)
    account = AccountSerializer(read_only=True)
    account_id = serializers.UUIDField(source='account.uuid', write_only=True)
    
    class Meta:
        model = JournalEntryLine
        fields = '__all__'
        read_only_fields = ('uuid',)


class LedgerSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    account_id = serializers.UUIDField(source='account.uuid', write_only=True)
    created_by = serializers.StringField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Ledger
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class BankAccountSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    account_id = serializers.UUIDField(source='account.uuid', write_only=True)
    
    class Meta:
        model = BankAccount
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'current_balance')


class BankTransactionSerializer(serializers.ModelSerializer):
    bank_account = BankAccountSerializer(read_only=True)
    bank_account_id = serializers.UUIDField(source='bank_account.uuid', write_only=True)
    reconciled_by = serializers.StringField(source='reconciled_by.get_full_name', read_only=True)
    reconciled_by_id = serializers.UUIDField(source='reconciled_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = BankTransaction
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'reconciled_at', 'net_amount')


class TrialBalanceSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    account_id = serializers.UUIDField(source='account.uuid', write_only=True)
    
    class Meta:
        model = TrialBalance
        fields = '__all__'
        read_only_fields = ('uuid',)


class FinancialStatementSerializer(serializers.ModelSerializer):
    generated_by = serializers.StringField(source='generated_by.get_full_name', read_only=True)
    generated_by_id = serializers.UUIDField(source='generated_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = FinancialStatement
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')
