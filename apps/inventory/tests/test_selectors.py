"""
Tests for inventory selectors
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization, OrganizationMembership
from apps.branches.models import Branch, BranchUserAccess
from apps.inventory.models import Product, Category, Warehouse, ProductUnit
from apps.inventory.selectors import InventorySelector

User = get_user_model()


class TestInventorySelectors(TestCase):
    """Test inventory selectors"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        OrganizationMembership.objects.create(
            user=self.user,
            organization=self.org,
            is_active=True
        )
        BranchUserAccess.objects.create(
            user=self.user,
            branch=self.branch,
            is_active=True
        )
        
        self.category = Category.objects.create(
            name='Test Category',
            code='TC',
            organization=self.org
        )
        self.unit = ProductUnit.objects.create(
            name='Test Unit',
            code='TU',
            organization=self.org
        )
        self.product = Product.objects.create(
            name='Test Product',
            code='TP',
            category=self.category,
            unit=self.unit,
            organization=self.org,
            branch=self.branch
        )
        self.warehouse = Warehouse.objects.create(
            name='Test Warehouse',
            code='TW',
            organization=self.org,
            branch=self.branch
        )
    
    def test_get_products(self):
        """Test getting products through selector"""
        request = self.create_request(self.user)
        selector = InventorySelector(request)
        products = selector.get_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['name'], 'Test Product')
    
    def test_get_warehouses(self):
        """Test getting warehouses through selector"""
        request = self.create_request(self.user)
        selector = InventorySelector(request)
        warehouses = selector.get_warehouses()
        self.assertEqual(len(warehouses), 1)
        self.assertEqual(warehouses[0]['name'], 'Test Warehouse')
    
    def create_request(self, user):
        """Helper to create a request with user, org, and branch"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/test/')
        request.user = user
        request.organization = self.org
        request.branch = self.branch
        return request
