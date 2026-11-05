"""
Tests for Inventory models
"""
import pytest
from django.test import TestCase
from apps.inventory.models import (
    Warehouse, ProductCategory, ProductBrand, UnitOfMeasure,
    Product, ProductSerialNumber, StockMovement, StockTransfer,
    StockTransferItem, StockAdjustment, StockAdjustmentItem,
    Service, ServiceCategory
)


class TestWarehouse(TestCase):
    """Test Warehouse model"""
    
    def test_warehouse_creation(self):
        """Test creating a warehouse"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        manager = User.objects.create_user(username='manager', email='manager@test.com')
        
        warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            code='MW',
            manager=manager,
            location='123 Warehouse St',
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(warehouse.name, 'Main Warehouse')
        self.assertEqual(warehouse.code, 'MW')


class TestProductCategory(TestCase):
    """Test ProductCategory model"""
    
    def test_product_category_creation(self):
        """Test creating a product category"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        category = ProductCategory.objects.create(
            name='Electronics',
            code='ELEC',
            description='Electronic products',
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(category.name, 'Electronics')


class TestProductBrand(TestCase):
    """Test ProductBrand model"""
    
    def test_product_brand_creation(self):
        """Test creating a product brand"""
        brand = ProductBrand.objects.create(
            name='Samsung',
            code='SAM',
            description='Samsung brand',
            website='https://www.samsung.com',
            is_active=True
        )
        self.assertEqual(brand.name, 'Samsung')


class TestUnitOfMeasure(TestCase):
    """Test UnitOfMeasure model"""
    
    def test_uom_creation(self):
        """Test creating a unit of measure"""
        uom = UnitOfMeasure.objects.create(
            name='Piece',
            code='PCS',
            symbol='pc',
            is_active=True
        )
        self.assertEqual(uom.name, 'Piece')
        self.assertEqual(uom.symbol, 'pc')


class TestProduct(TestCase):
    """Test Product model"""
    
    def test_product_creation(self):
        """Test creating a product"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        category = ProductCategory.objects.create(name='Electronics', code='ELEC', organization=org, branch=branch)
        brand = ProductBrand.objects.create(name='Samsung', code='SAM')
        uom = UnitOfMeasure.objects.create(name='Piece', code='PCS')
        
        product = Product.objects.create(
            sku='SAM-GS23-001',
            name='Samsung Galaxy S23',
            barcode='123456789012',
            category=category,
            brand=brand,
            uom=uom,
            unit_cost=800.00,
            selling_price=1000.00,
            initial_stock=10,
            current_stock=10,
            minimum_stock=5,
            maximum_stock=100,
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(product.sku, 'SAM-GS23-001')
        self.assertEqual(product.name, 'Samsung Galaxy S23')


class TestService(TestCase):
    """Test Service model"""
    
    def test_service_creation(self):
        """Test creating a service"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        
        service = Service.objects.create(
            service_number='SVC001',
            name='Screen Repair',
            description='LCD screen replacement service',
            duration=60,
            price=150.00,
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(service.name, 'Screen Repair')
        self.assertEqual(service.price, 150.00)
