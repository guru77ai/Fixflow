"""
Tests for suppliers selectors
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization, OrganizationMembership
from apps.branches.models import Branch, BranchUserAccess
from apps.suppliers.models import Supplier, SupplierCategory
from apps.suppliers.selectors import SupplierSelector

User = get_user_model()


class TestSuppliersSelectors(TestCase):
    """Test suppliers selectors"""
    
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
        
        self.category = SupplierCategory.objects.create(
            name='Test Category',
            code='TC',
            organization=self.org
        )
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            code='TS',
            category=self.category,
            organization=self.org,
            branch=self.branch
        )
    
    def test_get_suppliers(self):
        """Test getting suppliers through selector"""
        request = self.create_request(self.user)
        selector = SupplierSelector(request)
        suppliers = selector.get_suppliers()
        self.assertEqual(len(suppliers), 1)
        self.assertEqual(suppliers[0]['name'], 'Test Supplier')
    
    def test_get_supplier_categories(self):
        """Test getting supplier categories through selector"""
        request = self.create_request(self.user)
        selector = SupplierSelector(request)
        categories = selector.get_supplier_categories()
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0]['name'], 'Test Category')
    
    def create_request(self, user):
        """Helper to create a request with user, org, and branch"""
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/test/')
        request.user = user
        request.organization = self.org
        request.branch = self.branch
        return request
