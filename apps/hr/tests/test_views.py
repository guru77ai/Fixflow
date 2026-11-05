"""
Tests for HR views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.hr.models import Department, Position, EmploymentType

User = get_user_model()


class TestDepartmentViews(TestCase):
    """Test Department views"""
    
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
        self.department = Department.objects.create(
            name='Repair Department',
            code='REPAIR',
            description='Handles all device repair operations',
            organization=self.org,
            branch=self.branch
        )
    
    def test_department_list_view(self):
        """Test department list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('hr:department_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Departments')


class TestPositionViews(TestCase):
    """Test Position views"""
    
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
        self.department = Department.objects.create(
            name='Repair Department',
            code='REPAIR',
            organization=self.org,
            branch=self.branch
        )
        self.position = Position.objects.create(
            name='Technician',
            code='TECHNICIAN',
            description='Device repair technician',
            department=self.department,
            level=1,
            organization=self.org,
            branch=self.branch
        )
    
    def test_position_list_view(self):
        """Test position list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('hr:position_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Positions')


class TestEmploymentTypeViews(TestCase):
    """Test EmploymentType views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.employment_type = EmploymentType.objects.create(
            name='Full-time',
            code='FULL_TIME',
            description='Full-time employment'
        )
    
    def test_employment_type_list_view(self):
        """Test employment type list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('hr:employment_type_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Employment Types')
