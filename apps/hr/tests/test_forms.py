"""
Tests for HR forms
"""
from django.test import TestCase
from apps.hr.forms import (
    DepartmentForm, PositionForm, EmploymentTypeForm,
    EmployeeForm, LeaveTypeForm, LeaveRequestForm
)
from apps.hr.models import Department
from apps.core.models import Organization, Branch


class TestDepartmentForm(TestCase):
    """Test DepartmentForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_department_form_valid_data(self):
        """Test department form with valid data"""
        data = {
            'name': 'Repair Department',
            'code': 'REPAIR',
            'description': 'Handles all device repair operations',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = DepartmentForm(data=data)
        self.assertTrue(form.is_valid())


class TestPositionForm(TestCase):
    """Test PositionForm"""
    
    def setUp(self):
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
    
    def test_position_form_valid_data(self):
        """Test position form with valid data"""
        data = {
            'name': 'Technician',
            'code': 'TECHNICIAN',
            'description': 'Device repair technician',
            'department': self.department.uuid,
            'level': 1,
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = PositionForm(data=data)
        self.assertTrue(form.is_valid())


class TestEmploymentTypeForm(TestCase):
    """Test EmploymentTypeForm"""
    
    def test_employment_type_form_valid_data(self):
        """Test employment type form with valid data"""
        data = {
            'name': 'Full-time',
            'code': 'FULL_TIME',
            'description': 'Full-time employment'
        }
        form = EmploymentTypeForm(data=data)
        self.assertTrue(form.is_valid())
