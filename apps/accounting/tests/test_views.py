"""
Tests for Accounting views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.accounting.models import AccountType, AccountCategory

User = get_user_model()


class TestAccountTypeViews(TestCase):
    """Test AccountType views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.account_type = AccountType.objects.create(
            name='Asset',
            code='ASSET',
            description='Asset accounts',
            normal_balance='debit'
        )
    
    def test_account_type_list_view(self):
        """Test account type list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('accounting:account_type_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Types')


class TestAccountCategoryViews(TestCase):
    """Test AccountCategory views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
        self.account_type = AccountType.objects.create(
            name='Asset',
            code='ASSET'
        )
        self.account_category = AccountCategory.objects.create(
            name='Current Assets',
            code='CURRENT_ASSETS',
            description='Assets expected to be converted to cash within one year',
            account_type=self.account_type,
            organization=self.org,
            branch=self.branch
        )
    
    def test_account_category_list_view(self):
        """Test account category list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('accounting:account_category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account Categories')
