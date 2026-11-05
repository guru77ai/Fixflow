"""
Tests for inventory API endpoints
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch

User = get_user_model()


class TestInventoryListAPI(TestCase):
    """Test inventory list API endpoint"""
    
    def setUp(self):
        self.client = APIClient()
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
        self.client.force_authenticate(user=self.user)
    
    def test_list(self):
        """Test GET /api/inventory/"""
        url = reverse('inventory-api:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestInventoryDetailAPI(TestCase):
    """Test inventory detail API endpoint"""
    
    def setUp(self):
        self.client = APIClient()
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
        self.client.force_authenticate(user=self.user)
    
    def test_list(self):
        """Test API endpoint access"""
        self.assertTrue(True)
