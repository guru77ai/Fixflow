"""
Tests for Inventory views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.inventory.models import (
    Warehouse, ProductCategory, ProductBrand, UnitOfMeasure,
    Product
)

User = get_user_model()


class TestWarehouseViews(TestCase):
    """Test Warehouse views"""
    
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
        self.warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            code='MAIN_WH',
            address='123 Warehouse St',
            phone='1234567890',
            email='warehouse@test.com',
            organization=self.org,
            branch=self.branch
        )
    
    def test_warehouse_list_view(self):
        """Test warehouse list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:warehouse_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Warehouses')
    
    def test_warehouse_detail_view(self):
        """Test warehouse detail view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:warehouse_detail', args=[self.warehouse.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Main Warehouse')
    
    def test_warehouse_create_view(self):
        """Test warehouse create view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:warehouse_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Warehouse')
    
    def test_warehouse_update_view(self):
        """Test warehouse update view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:warehouse_update', args=[self.warehouse.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Warehouse')
    
    def test_warehouse_delete_view(self):
        """Test warehouse delete view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:warehouse_delete', args=[self.warehouse.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirm Deletion')


class TestProductViews(TestCase):
    """Test Product views"""
    
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
        self.warehouse = Warehouse.objects.create(
            name='Main Warehouse',
            code='MAIN_WH',
            organization=self.org,
            branch=self.branch
        )
        self.category = ProductCategory.objects.create(
            name='Parts',
            code='PARTS',
            organization=self.org,
            branch=self.branch
        )
        self.brand = ProductBrand.objects.create(
            name='Generic',
            code='GENERIC'
        )
        self.unit = UnitOfMeasure.objects.create(
            name='Piece',
            code='PCS'
        )
        self.product = Product.objects.create(
            code='PROD001',
            name='Test Product',
            category=self.category,
            brand=self.brand,
            unit=self.unit,
            current_stock=10.000,
            purchase_price=50.00,
            selling_price=100.00,
            organization=self.org,
            branch=self.branch
        )
    
    def test_product_list_view(self):
        """Test product list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Products')
    
    def test_product_detail_view(self):
        """Test product detail view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:product_detail', args=[self.product.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_product_create_view(self):
        """Test product create view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('inventory:product_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Product')
