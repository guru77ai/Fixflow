"""
Tests for Accounting forms
"""
from django.test import TestCase
from apps.accounting.forms import (
    AccountTypeForm, AccountCategoryForm, AccountForm,
    JournalEntryForm, BankAccountForm
)


class TestAccountTypeForm(TestCase):
    """Test AccountTypeForm"""
    
    def test_account_type_form_valid_data(self):
        """Test account type form with valid data"""
        data = {
            'name': 'Asset',
            'code': 'ASSET',
            'description': 'Asset accounts',
            'normal_balance': 'debit'
        }
        form = AccountTypeForm(data=data)
        self.assertTrue(form.is_valid())


class TestAccountCategoryForm(TestCase):
    """Test AccountCategoryForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_account_category_form_valid_data(self):
        """Test account category form with valid data"""
        data = {
            'name': 'Current Assets',
            'code': 'CURRENT_ASSETS',
            'description': 'Assets expected to be converted to cash within one year',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = AccountCategoryForm(data=data)
        self.assertTrue(form.is_valid())
