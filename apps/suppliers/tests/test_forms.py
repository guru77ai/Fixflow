"""
Tests for Suppliers forms
"""
from django.test import TestCase
from apps.suppliers.forms import SupplierForm, SupplierCategoryForm, SupplierContactForm
from apps.core.models import Organization, Branch


class TestSupplierCategoryForm(TestCase):
    """Test SupplierCategoryForm"""
    
    def test_supplier_category_form_valid_data(self):
        """Test supplier category form with valid data"""
        data = {
            'name': 'Parts Supplier',
            'code': 'PARTS'
        }
        form = SupplierCategoryForm(data=data)
        self.assertTrue(form.is_valid())


class TestSupplierForm(TestCase):
    """Test SupplierForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_supplier_form_valid_data(self):
        """Test supplier form with valid data"""
        data = {
            'name': 'TechParts Ltd',
            'supplier_number': 'SUP001',
            'code': 'TECHPARTS',
            'email': 'sales@techparts.com',
            'phone': '1234567890',
            'address': '123 Tech Street',
            'city': 'Tech City',
            'state': 'TC',
            'postal_code': '12345',
            'country': 'USA',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = SupplierForm(data=data)
        self.assertTrue(form.is_valid())


class TestSupplierContactForm(TestCase):
    """Test SupplierContactForm"""
    
    def test_supplier_contact_form_valid_data(self):
        """Test supplier contact form with valid data"""
        data = {
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'john@techparts.com',
            'phone': '1234567890'
        }
        form = SupplierContactForm(data=data)
        self.assertTrue(form.is_valid())
