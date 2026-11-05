"""
Tests for Suppliers models
"""
import pytest
from django.test import TestCase
from apps.suppliers.models import SupplierCategory, Supplier, SupplierContact, SupplierDocument


class TestSupplierCategory(TestCase):
    """Test SupplierCategory model"""
    
    def test_supplier_category_creation(self):
        """Test creating a supplier category"""
        category = SupplierCategory.objects.create(
            name='Electronics',
            code='ELEC',
            description='Electronic suppliers',
            sequence=1,
            is_active=True
        )
        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(category.code, 'ELEC')


class TestSupplier(TestCase):
    """Test Supplier model"""
    
    def test_supplier_creation(self):
        """Test creating a supplier"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        category = SupplierCategory.objects.create(name='Electronics', code='ELEC')
        
        supplier = Supplier.objects.create(
            name='Tech Supplier Inc.',
            supplier_number='SUP001',
            category=category,
            email='contact@techsupplier.com',
            phone='1234567890',
            address='123 Supplier St',
            city='Tech City',
            state='TC',
            postal_code='12345',
            country='USA',
            tax_id='TAX123',
            website='https://www.techsupplier.com',
            payment_terms='Net 30',
            credit_limit=10000.00,
            organization=org,
            branch=branch,
            status='active',
            is_active=True
        )
        self.assertEqual(supplier.name, 'Tech Supplier Inc.')
        self.assertEqual(supplier.email, 'contact@techsupplier.com')


class TestSupplierContact(TestCase):
    """Test SupplierContact model"""
    
    def test_supplier_contact_creation(self):
        """Test creating a supplier contact"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        supplier = Supplier.objects.create(
            name='Tech Supplier Inc.',
            supplier_number='SUP001',
            organization=org,
            branch=branch
        )
        
        contact = SupplierContact.objects.create(
            supplier=supplier,
            first_name='John',
            last_name='Smith',
            email='john@techsupplier.com',
            phone='9876543210',
            mobile='5551234567',
            position='Sales Manager',
            is_primary=True
        )
        self.assertEqual(contact.full_name, 'John Smith')
        self.assertEqual(contact.position, 'Sales Manager')
