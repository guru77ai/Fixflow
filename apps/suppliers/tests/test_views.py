"""
Tests for Suppliers views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.suppliers.models import SupplierCategory, Supplier

User = get_user_model()


class TestSupplierCategoryViews(TestCase):
    """Test SupplierCategory views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = SupplierCategory.objects.create(
            name='Parts Supplier',
            code='PARTS'
        )
    
    def test_supplier_category_list_view(self):
        """Test supplier category list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('suppliers:supplier_category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Supplier Categories')


class TestSupplierViews(TestCase):
    """Test Supplier views"""
    
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
        self.category = SupplierCategory.objects.create(
            name='Parts Supplier',
            code='PARTS'
        )
        self.supplier = Supplier.objects.create(
            name='TechParts Ltd',
            supplier_number='SUP001',
            code='TECHPARTS',
            email='sales@techparts.com',
            phone='1234567890',
            address='123 Tech Street',
            city='Tech City',
            state='TC',
            postal_code='12345',
            country='USA',
            organization=self.org,
            branch=self.branch
        )
    
    def test_supplier_list_view(self):
        """Test supplier list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('suppliers:supplier_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Suppliers')
    
    def test_supplier_detail_view(self):
        """Test supplier detail view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('suppliers:supplier_detail', args=[self.supplier.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TechParts Ltd')
    
    def test_supplier_create_view(self):
        """Test supplier create view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('suppliers:supplier_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Supplier')
