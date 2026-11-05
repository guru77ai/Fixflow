"""
Tests for Accounting models
"""
import pytest
from django.test import TestCase
from apps.accounting.models import (
    AccountType, AccountCategory, ChartOfAccounts, Account,
    JournalEntry, JournalEntryLine, Ledger, BankAccount,
    BankTransaction, TrialBalance, FinancialStatement
)


class TestAccountType(TestCase):
    """Test AccountType model"""
    
    def test_account_type_creation(self):
        """Test creating an account type"""
        account_type = AccountType.objects.create(
            name='Asset',
            code='ASSET',
            normal_balance='debit',
            description='Asset accounts'
        )
        self.assertEqual(account_type.name, 'Asset')
        self.assertEqual(account_type.normal_balance, 'debit')


class TestAccountCategory(TestCase):
    """Test AccountCategory model"""
    
    def test_account_category_creation(self):
        """Test creating an account category"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        account_type = AccountType.objects.create(name='Asset', code='ASSET')
        
        category = AccountCategory.objects.create(
            name='Current Assets',
            code='CA',
            account_type=account_type,
            description='Current asset accounts',
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(category.name, 'Current Assets')


class TestChartOfAccounts(TestCase):
    """Test ChartOfAccounts model"""
    
    def test_chart_of_accounts_creation(self):
        """Test creating a chart of accounts"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        chart = ChartOfAccounts.objects.create(
            name='Standard Chart',
            code='STD',
            description='Standard chart of accounts',
            organization=org,
            branch=branch,
            is_active=True,
            is_default=True
        )
        self.assertEqual(chart.name, 'Standard Chart')


class TestAccount(TestCase):
    """Test Account model"""
    
    def test_account_creation(self):
        """Test creating an account"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        account_type = AccountType.objects.create(name='Asset', code='ASSET')
        chart = ChartOfAccounts.objects.create(name='Standard', code='STD', organization=org, branch=branch)
        
        account = Account.objects.create(
            code='1000',
            name='Cash',
            chart_of_accounts=chart,
            account_type=account_type,
            description='Cash account',
            opening_balance=1000.00,
            current_balance=1000.00,
            status='active',
            is_bank=False,
            is_cash=True,
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(account.code, '1000')
        self.assertEqual(account.name, 'Cash')


class TestJournalEntry(TestCase):
    """Test JournalEntry model"""
    
    def test_journal_entry_creation(self):
        """Test creating a journal entry"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        user = User.objects.create_user(username='accountant', email='accountant@test.com')
        
        entry = JournalEntry.objects.create(
            entry_number='JE001',
            reference='INV001',
            description='Invoice payment',
            entry_date='2023-01-01',
            created_by=user,
            is_posted=False,
            organization=org,
            branch=branch
        )
        self.assertEqual(entry.entry_number, 'JE001')
        self.assertEqual(entry.description, 'Invoice payment')


class TestBankAccount(TestCase):
    """Test BankAccount model"""
    
    def test_bank_account_creation(self):
        """Test creating a bank account"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        account_type = AccountType.objects.create(name='Asset', code='ASSET')
        chart = ChartOfAccounts.objects.create(name='Standard', code='STD', organization=org, branch=branch)
        account = Account.objects.create(
            code='1010',
            name='Bank Account',
            chart_of_accounts=chart,
            account_type=account_type,
            organization=org,
            branch=branch
        )
        
        bank_account = BankAccount.objects.create(
            account=account,
            bank_name='Test Bank',
            branch_name='Main Branch',
            account_number='1234567890',
            account_holder='Test Company',
            current_balance=5000.00,
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(bank_account.bank_name, 'Test Bank')
        self.assertEqual(bank_account.account_number, '1234567890')


class TestBankTransaction(TestCase):
    """Test BankTransaction model"""
    
    def test_bank_transaction_creation(self):
        """Test creating a bank transaction"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        account_type = AccountType.objects.create(name='Asset', code='ASSET')
        chart = ChartOfAccounts.objects.create(name='Standard', code='STD', organization=org, branch=branch)
        account = Account.objects.create(
            code='1010',
            name='Bank Account',
            chart_of_accounts=chart,
            account_type=account_type,
            organization=org,
            branch=branch
        )
        bank_account = BankAccount.objects.create(
            account=account,
            bank_name='Test Bank',
            account_number='1234567890',
            organization=org,
            branch=branch
        )
        user = User.objects.create_user(username='accountant', email='accountant@test.com')
        
        transaction = BankTransaction.objects.create(
            bank_account=bank_account,
            transaction_type='deposit',
            transaction_number='TXN001',
            reference='DEP001',
            description='Customer deposit',
            amount=1000.00,
            fee=0.00,
            net_amount=1000.00,
            transaction_date='2023-01-01',
            is_reconciled=False,
            reconciled_by=user,
            organization=org,
            branch=branch
        )
        self.assertEqual(transaction.transaction_type, 'deposit')
        self.assertEqual(transaction.amount, 1000.00)
