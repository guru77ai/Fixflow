"""
Tests for Inventory forms
"""
from django.test import TestCase
from apps.inventory.forms import (
    WarehouseForm, ProductCategoryForm, ProductBrandForm,
    UnitOfMeasureForm, ProductForm
)
from apps.core.models import Organization, Branch


class TestWarehouseForm(TestCase):
    """Test WarehouseForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_warehouse_form_valid_data(self):
        """Test warehouse form with valid data"""
        data = {
            'name': 'Main Warehouse',
            'code': 'MAIN_WH',
            'address': '123 Warehouse St',
            'phone': '1234567890',
            'email': 'warehouse@test.com',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = WarehouseForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_warehouse_form_required_fields(self):
        """Test that required fields are enforced"""
        data = {
            'name': '',
            'code': ''
        }
        form = WarehouseForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('code', form.errors)


class TestProductCategoryForm(TestCase):
    """Test ProductCategoryForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_product_category_form_valid_data(self):
        """Test product category form with valid data"""
        data = {
            'name': 'Parts',
            'code': 'PARTS',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = ProductCategoryForm(data=data)
        self.assertTrue(form.is_valid())


class TestProductBrandForm(TestCase):
    """Test ProductBrandForm"""
    
    def test_product_brand_form_valid_data(self):
        """Test product brand form with valid data"""
        data = {
            'name': 'Generic',
            'code': 'GENERIC'
        }
        form = ProductBrandForm(data=data)
        self.assertTrue(form.is_valid())


class TestUnitOfMeasureForm(TestCase):
    """Test UnitOfMeasureForm"""
    
    def test_unit_of_measure_form_valid_data(self):
        """Test unit of measure form with valid data"""
        data = {
            'name': 'Piece',
            'code': 'PCS'
        }
        form = UnitOfMeasureForm(data=data)
        self.assertTrue(form.is_valid())
