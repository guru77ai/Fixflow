"""
Tests for POS views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.pos.models import PaymentMethod, CashRegister, Sale

User = get_user_model()


class TestPaymentMethodViews(TestCase):
    """Test PaymentMethod views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.payment_method = PaymentMethod.objects.create(
            name='Cash',
            code='CASH',
            description='Cash payment',
            is_active=True
        )
    
    def test_payment_method_list_view(self):
        """Test payment method list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pos:payment_method_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payment Methods')


class TestCashRegisterViews(TestCase):
    """Test CashRegister views"""
    
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
        self.cash_register = CashRegister.objects.create(
            name='Register 1',
            code='REG001',
            description='Main cash register',
            initial_balance=1000.00,
            daily_target=5000.00,
            organization=self.org,
            branch=self.branch
        )
    
    def test_cash_register_list_view(self):
        """Test cash register list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pos:cash_register_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cash Registers')


class TestSaleViews(TestCase):
    """Test Sale views"""
    
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
        self.payment_method = PaymentMethod.objects.create(
            name='Cash',
            code='CASH'
        )
        self.cash_register = CashRegister.objects.create(
            name='Register 1',
            code='REG001',
            organization=self.org,
            branch=self.branch
        )
        self.sale = Sale.objects.create(
            sale_number='SALE001',
            subtotal=100.00,
            tax_amount=10.00,
            discount=0.00,
            total=110.00,
            organization=self.org,
            branch=self.branch
        )
    
    def test_sale_list_view(self):
        """Test sale list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pos:sale_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sales')
    
    def test_sale_detail_view(self):
        """Test sale detail view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('pos:sale_detail', args=[self.sale.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SALE001')
