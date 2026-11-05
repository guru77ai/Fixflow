"""
Tests for Financial forms
"""
from django.test import TestCase
from apps.financial.forms import (
    InvoiceStatusForm, InvoiceTypeForm, InvoiceForm,
    PaymentForm, ExpenseCategoryForm, ExpenseForm
)


class TestInvoiceStatusForm(TestCase):
    """Test InvoiceStatusForm"""
    
    def test_invoice_status_form_valid_data(self):
        """Test invoice status form with valid data"""
        data = {
            'name': 'Draft',
            'code': 'draft',
            'description': 'Invoice is being prepared',
            'color': '#999999',
            'sequence': 1
        }
        form = InvoiceStatusForm(data=data)
        self.assertTrue(form.is_valid())


class TestInvoiceTypeForm(TestCase):
    """Test InvoiceTypeForm"""
    
    def test_invoice_type_form_valid_data(self):
        """Test invoice type form with valid data"""
        data = {
            'name': 'Repair Invoice',
            'code': 'REPAIR',
            'description': 'Invoice for repair services',
            'prefix': 'REP-INV',
            'is_active': True
        }
        form = InvoiceTypeForm(data=data)
        self.assertTrue(form.is_valid())


class TestExpenseCategoryForm(TestCase):
    """Test ExpenseCategoryForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_expense_category_form_valid_data(self):
        """Test expense category form with valid data"""
        data = {
            'name': 'Office Supplies',
            'code': 'OFFICE',
            'description': 'Office supply expenses',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = ExpenseCategoryForm(data=data)
        self.assertTrue(form.is_valid())
