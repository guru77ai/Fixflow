"""
Tests for POS forms
"""
from django.test import TestCase
from apps.pos.forms import SaleForm, CashRegisterForm, PaymentMethodForm
from apps.core.models import Organization, Branch


class TestPaymentMethodForm(TestCase):
    """Test PaymentMethodForm"""
    
    def test_payment_method_form_valid_data(self):
        """Test payment method form with valid data"""
        data = {
            'name': 'Cash',
            'code': 'CASH',
            'description': 'Cash payment',
            'is_active': True
        }
        form = PaymentMethodForm(data=data)
        self.assertTrue(form.is_valid())


class TestCashRegisterForm(TestCase):
    """Test CashRegisterForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_cash_register_form_valid_data(self):
        """Test cash register form with valid data"""
        data = {
            'name': 'Register 1',
            'code': 'REG001',
            'description': 'Main cash register',
            'initial_balance': 1000.00,
            'daily_target': 5000.00,
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = CashRegisterForm(data=data)
        self.assertTrue(form.is_valid())


class TestSaleForm(TestCase):
    """Test SaleForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_sale_form_valid_data(self):
        """Test sale form with valid data"""
        data = {
            'sale_number': 'SALE001',
            'subtotal': 100.00,
            'tax_amount': 10.00,
            'discount': 0.00,
            'total': 110.00,
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = SaleForm(data=data)
        self.assertTrue(form.is_valid())
