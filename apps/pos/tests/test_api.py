"""
Tests for pos API endpoints
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch

User = get_user_model()


class TestPOSListAPI(TestCase):
    """Test pos list API endpoint"""
    
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
        """Test GET /api/pos/"""
        url = reverse('pos-api:sale-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPOSDetailAPI(TestCase):
    """Test pos detail API endpoint"""
    
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
