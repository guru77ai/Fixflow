"""
Tests for Repair views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.crm.models import Customer, Device, DeviceBrand, DeviceModel
from apps.repair.models import (
    RepairStatus, RepairPriority, RepairCategory, RepairType,
    RepairOrder, RepairTemplate
)

User = get_user_model()


class TestRepairStatusViews(TestCase):
    """Test RepairStatus view"""
    
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
        self.status = RepairStatus.objects.create(
            name='Received',
            code='RCV',
            description='Device received',
            sequence=1,
            color='#FF0000'
        )
    
    def test_repair_status_list_view(self):
        """Test repair status list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_status_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Repair Statuses')
    
    def test_repair_status_create_view(self):
        """Test repair status create view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_status_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Repair Status')
    
    def test_repair_status_create_post(self):
        """Test repair status create POST"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_status_create')
        data = {
            'name': 'In Progress',
            'code': 'INP',
            'description': 'Device in progress',
            'sequence': 2,
            'color': '#00FF00',
            'is_initial': False,
            'is_final': False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RepairStatus.objects.filter(code='INP').exists())
    
    def test_repair_status_update_view(self):
        """Test repair status update view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_status_update', args=[self.status.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Repair Status')
    
    def test_repair_status_delete_view(self):
        """Test repair status delete view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_status_delete', args=[self.status.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirm Deletion')


class TestRepairPriorityViews(TestCase):
    """Test RepairPriority view"""
    
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
        self.priority = RepairPriority.objects.create(
            name='High',
            code='HIGH',
            level=1,
            estimated_hours=24,
            color='#FF0000'
        )
    
    def test_repair_priority_list_view(self):
        """Test repair priority list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_priority_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Repair Priorities')


class TestRepairCategoryViews(TestCase):
    """Test RepairCategory view"""
    
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
        self.category = RepairCategory.objects.create(
            name='Hardware',
            code='HW',
            description='Hardware repairs',
            color='#0000FF'
        )
    
    def test_repair_category_list_view(self):
        """Test repair category list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Repair Categories')


class TestRepairTypeViews(TestCase):
    """Test RepairType view"""
    
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
        self.category = RepairCategory.objects.create(
            name='Hardware',
            code='HW'
        )
        self.repair_type = RepairType.objects.create(
            name='Screen Replacement',
            code='SCR',
            category=self.category,
            estimated_cost=100.00,
            estimated_duration=60
        )
    
    def test_repair_type_list_view(self):
        """Test repair type list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_type_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Repair Types')


class TestRepairOrderViews(TestCase):
    """Test RepairOrder view"""
    
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
    
    def test_repair_order_list_view(self):
        """Test repair order list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_order_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Repair Orders')
    
    def test_repair_order_detail_view(self):
        """Test repair order detail view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_order_detail', args=[self.repair_order.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'REP001')
    
    def test_repair_order_create_view(self):
        """Test repair order create view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('repair:repair_order_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add Repair Order')
