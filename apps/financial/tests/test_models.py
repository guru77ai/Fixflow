"""
Tests for Financial models
"""
import pytest
from django.test import TestCase
from apps.financial.models import (
    InvoiceStatus, InvoiceType, Invoice, InvoiceItem, InvoicePayment,
    Payment, PaymentMethod, Expense, ExpenseCategory, TaxRate,
    BudgetCategory, Budget, Currency
)


class TestInvoiceStatus(TestCase):
    """Test InvoiceStatus model"""
    
    def test_invoice_status_creation(self):
        """Test creating an invoice status"""
        status = InvoiceStatus.objects.create(
            name='Draft',
            code='DRAFT',
            sequence=1,
            is_default=True,
            is_final=False
        )
        self.assertEqual(status.name, 'Draft')
        self.assertEqual(status.code, 'DRAFT')


class TestInvoiceType(TestCase):
    """Test InvoiceType model"""
    
    def test_invoice_type_creation(self):
        """Test creating an invoice type"""
        invoice_type = InvoiceType.objects.create(
            name='Sales Invoice',
            code='SALES',
            prefix='INV',
            description='Sales invoice'
        )
        self.assertEqual(invoice_type.name, 'Sales Invoice')
        self.assertEqual(invoice_type.prefix, 'INV')


class TestInvoice(TestCase):
    """Test Invoice model"""
    
    def test_invoice_creation(self):
        """Test creating an invoice"""
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
        
        invoice_type = InvoiceType.objects.create(name='Sales', code='SALES', prefix='INV')
        status = InvoiceStatus.objects.create(name='Draft', code='DRAFT', is_default=True)
        user = User.objects.create_user(username='accountant', email='accountant@test.com')
        
        invoice = Invoice.objects.create(
            invoice_number='INV001',
            invoice_type=invoice_type,
            status=status,
            customer=customer,
            reference='ORDER001',
            reference_type='sales_order',
            subtotal=100.00,
            discount=0.00,
            tax_amount=10.00,
            total_amount=110.00,
            amount_paid=0.00,
            balance=110.00,
            payment_status='pending',
            due_date='2023-02-01',
            is_recurring=False,
            created_by=user,
            organization=org,
            branch=branch
        )
        self.assertEqual(invoice.invoice_number, 'INV001')
        self.assertEqual(invoice.total_amount, 110.00)


class TestPaymentMethod(TestCase):
    """Test PaymentMethod model"""
    
    def test_payment_method_creation(self):
        """Test creating a payment method"""
        payment_method = PaymentMethod.objects.create(
            name='Credit Card',
            code='CC',
            type='card',
            description='Credit card payment',
            sequence=1,
            is_active=True
        )
        self.assertEqual(payment_method.name, 'Credit Card')
        self.assertEqual(payment_method.type, 'card')


class TestExpenseCategory(TestCase):
    """Test ExpenseCategory model"""
    
    def test_expense_category_creation(self):
        """Test creating an expense category"""
        category = ExpenseCategory.objects.create(
            name='Office Supplies',
            code='OFF',
            budget_code='OFF-SUP',
            description='Office supplies expenses',
            is_active=True
        )
        self.assertEqual(category.name, 'Office Supplies')


class TestExpense(TestCase):
    """Test Expense model"""
    
    def test_expense_creation(self):
        """Test creating an expense"""
        from apps.core.models import Organization, Branch
        from apps.suppliers.models import Supplier
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        category = ExpenseCategory.objects.create(name='Office Supplies', code='OFF')
        supplier = Supplier.objects.create(
            name='Office Supplier',
            supplier_number='SUP001',
            organization=org,
            branch=branch
        )
        payment_method = PaymentMethod.objects.create(name='Cash', code='CASH', type='cash')
        user = User.objects.create_user(username='accountant', email='accountant@test.com')
        
        expense = Expense.objects.create(
            expense_number='EXP001',
            category=category,
            title='Office Supplies Purchase',
            description='Monthly office supplies',
            amount=100.00,
            tax_amount=10.00,
            total_amount=110.00,
            currency='USD',
            payment_method=payment_method,
            payment_reference='REC001',
            expense_date='2023-01-01',
            paid_date='2023-01-01',
            supplier=supplier,
            status='approved',
            submitted_by=user,
            approved_by=user,
            paid_by=user,
            receipt_attached=True,
            organization=org,
            branch=branch
        )
        self.assertEqual(expense.expense_number, 'EXP001')
        self.assertEqual(expense.total_amount, 110.00)


class TestTaxRate(TestCase):
    """Test TaxRate model"""
    
    def test_tax_rate_creation(self):
        """Test creating a tax rate"""
        tax_rate = TaxRate.objects.create(
            name='VAT',
            code='VAT',
            rate=10.00,
            type='percentage',
            description='Value Added Tax',
            is_default=True,
            is_active=True
        )
        self.assertEqual(tax_rate.name, 'VAT')
        self.assertEqual(tax_rate.rate, 10.00)


class TestCurrency(TestCase):
    """Test Currency model"""
    
    def test_currency_creation(self):
        """Test creating a currency"""
        currency = Currency.objects.create(
            code='USD',
            name='US Dollar',
            symbol='$',
            is_active=True,
            is_default=True
        )
        self.assertEqual(currency.code, 'USD')
        self.assertEqual(currency.name, 'US Dollar')
