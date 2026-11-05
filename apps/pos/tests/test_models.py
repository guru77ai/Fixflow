"""
Tests for POS models
"""
import pytest
from django.test import TestCase
from apps.pos.models import (
    PaymentMethod, CashRegister, Sale, SaleItem, SalePayment,
    Receipt, Refund, RefundItem, POSSession, POSSettings
)


class TestPaymentMethod(TestCase):
    """Test PaymentMethod model"""
    
    def test_payment_method_creation(self):
        """Test creating a payment method"""
        payment_method = PaymentMethod.objects.create(
            name='Cash',
            code='CASH',
            type='cash',
            description='Cash payment',
            sequence=1,
            is_active=True
        )
        self.assertEqual(payment_method.name, 'Cash')
        self.assertEqual(payment_method.code, 'CASH')


class TestCashRegister(TestCase):
    """Test CashRegister model"""
    
    def test_cash_register_creation(self):
        """Test creating a cash register"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        cash_register = CashRegister.objects.create(
            name='Register 1',
            code='REG001',
            description='Main cash register',
            current_balance=1000.00,
            status='open',
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(cash_register.name, 'Register 1')
        self.assertEqual(cash_register.current_balance, 1000.00)


class TestSale(TestCase):
    """Test Sale model"""
    
    def test_sale_creation(self):
        """Test creating a sale"""
        from apps.core.models import Organization, Branch
        from apps.crm.models import Customer
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            organization=org,
            branch=branch
        )
        
        cash_register = CashRegister.objects.create(
            name='Register 1',
            code='REG001',
            organization=org,
            branch=branch
        )
        
        sale = Sale.objects.create(
            sale_number='SALE001',
            customer=customer,
            cash_register=cash_register,
            subtotal=100.00,
            tax_amount=10.00,
            discount=0.00,
            total_amount=110.00,
            amount_paid=110.00,
            balance=0.00,
            payment_status='paid',
            status='completed',
            sale_type='walk_in',
            organization=org,
            branch=branch
        )
        self.assertEqual(sale.sale_number, 'SALE001')
        self.assertEqual(sale.total_amount, 110.00)


class TestPOSSession(TestCase):
    """Test POSSession model"""
    
    def test_pos_session_creation(self):
        """Test creating a POS session"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        user = User.objects.create_user(username='cashier', email='cashier@test.com')
        
        cash_register = CashRegister.objects.create(
            name='Register 1',
            code='REG001',
            organization=org,
            branch=branch
        )
        
        session = POSSession.objects.create(
            session_number='SESSION001',
            cash_register=cash_register,
            user=user,
            start_time='2023-01-01T09:00:00',
            end_time='2023-01-01T17:00:00',
            status='closed',
            organization=org,
            branch=branch
        )
        self.assertEqual(session.session_number, 'SESSION001')
        self.assertEqual(session.status, 'closed')


class TestPOSSettings(TestCase):
    """Test POSSettings model"""
    
    def test_pos_settings_creation(self):
        """Test creating POS settings"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        settings = POSSettings.objects.create(
            default_receipt_type='printed',
            auto_print_receipt=True,
            show_customer_display=True,
            enable_tips=True,
            default_tax_rate=10.00,
            organization=org,
            branch=branch
        )
        self.assertTrue(settings.auto_print_receipt)
        self.assertTrue(settings.show_customer_display)
