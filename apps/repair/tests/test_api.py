"""
Tests for Repair API endpoints
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.crm.models import Customer, Device
from apps.repair.models import (
    RepairStatus, RepairPriority, RepairCategory, RepairType,
    RepairOrder
)

User = get_user_model()


class TestRepairStatusAPI(TestCase):
    """Test RepairStatus API endpoints"""
    
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
        self.status = RepairStatus.objects.create(
            name='Received',
            code='RCV',
            description='Device received',
            sequence=1,
            color='#FF0000'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_repair_status_list(self):
        """Test GET /api/repair/statuses/"""
        url = reverse('repair-api:repair_status-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_repair_status_create(self):
        """Test POST /api/repair/statuses/"""
        url = reverse('repair-api:repair_status-list')
        data = {
            'name': 'In Progress',
            'code': 'INP',
            'description': 'Device in progress',
            'sequence': 2,
            'color': '#00FF00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(RepairStatus.objects.filter(code='INP').exists())
    
    def test_repair_status_retrieve(self):
        """Test GET /api/repair/statuses/{uuid}/"""
        url = reverse('repair-api:repair_status-detail', args=[self.status.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Received')
    
    def test_repair_status_update(self):
        """Test PUT /api/repair/statuses/{uuid}/"""
        url = reverse('repair-api:repair_status-detail', args=[self.status.uuid])
        data = {
            'name': 'Received - Updated',
            'code': 'RCV',
            'description': 'Device received - updated',
            'sequence': 1,
            'color': '#FF0000'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Received - Updated')
    
    def test_repair_status_delete(self):
        """Test DELETE /api/repair/statuses/{uuid}/"""
        url = reverse('repair-api:repair_status-detail', args=[self.status.uuid])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RepairStatus.objects.filter(uuid=self.status.uuid).exists())


class TestRepairPriorityAPI(TestCase):
    """Test RepairPriority API endpoints"""
    
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
        self.priority = RepairPriority.objects.create(
            name='High',
            code='HIGH',
            level=1,
            estimated_hours=24,
            color='#FF0000'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_repair_priority_list(self):
        """Test GET /api/repair/priorities/"""
        url = reverse('repair-api:repair_priority-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class TestRepairCategoryAPI(TestCase):
    """Test RepairCategory API endpoints"""
    
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
        self.category = RepairCategory.objects.create(
            name='Hardware',
            code='HW',
            description='Hardware repairs',
            color='#0000FF',
            organization=self.org,
            branch=self.branch
        )
        self.client.force_authenticate(user=self.user)
    
    def test_repair_category_list(self):
        """Test GET /api/repair/categories/"""
        url = reverse('repair-api:repair_category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class TestRepairTypeAPI(TestCase):
    """Test RepairType API endpoints"""
    
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
        self.category = RepairCategory.objects.create(
            name='Hardware',
            code='HW',
            organization=self.org,
            branch=self.branch
        )
        self.repair_type = RepairType.objects.create(
            name='Screen Replacement',
            code='SCR',
            category=self.category,
            estimated_cost=100.00,
            estimated_duration=60
        )
        self.client.force_authenticate(user=self.user)
    
    def test_repair_type_list(self):
        """Test GET /api/repair/types/"""
        url = reverse('repair-api:repair_type-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)


class TestRepairOrderAPI(TestCase):
    """Test RepairOrder API endpoints"""
    
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
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            organization=self.org,
            branch=self.branch
        )
        self.device = Device.objects.create(
            name='Test Device',
            serial_number='SN001',
            imei='123456789012345',
            customer=self.customer,
            organization=self.org,
            branch=self.branch
        )
        self.status = RepairStatus.objects.create(
            name='Received',
            code='RCV'
        )
        self.priority = RepairPriority.objects.create(
            name='Medium',
            code='MED',
            level=2
        )
        self.repair_order = RepairOrder.objects.create(
            order_number='REP001',
            customer=self.customer,
            device=self.device,
            status=self.status,
            priority=self.priority,
            issue_description='Test issue',
            organization=self.org,
            branch=self.branch
        )
        self.client.force_authenticate(user=self.user)
    
    def test_repair_order_list(self):
        """Test GET /api/repair/orders/"""
        url = reverse('repair-api:repair_order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
    
    def test_repair_order_retrieve(self):
        """Test GET /api/repair/orders/{uuid}/"""
        url = reverse('repair-api:repair_order-detail', args=[self.repair_order.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_number'], 'REP001')
