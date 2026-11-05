"""
Tests for CRM forms
"""
from django.test import TestCase
from apps.crm.forms import (
    CustomerForm, DeviceForm, CustomerTypeForm, CustomerSourceForm,
    CustomerGroupForm, DeviceBrandForm, DeviceModelForm, DeviceCategoryForm
)
from apps.core.models import Organization, Branch
from apps.crm.models import Customer, Device


class TestCustomerForm(TestCase):
    """Test CustomerForm"""
    
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.branch = Branch.objects.create(
            name='Test Branch',
            code='TB',
            organization=self.org
        )
    
    def test_customer_form_valid_data(self):
        """Test customer form with valid data"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = CustomerForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_customer_form_required_fields(self):
        """Test that required fields are enforced"""
        data = {
            'first_name': '',
            'last_name': '',
            'email': ''
        }
        form = CustomerForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
    
    def test_customer_form_save(self):
        """Test saving customer form"""
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'phone': '9876543210',
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = CustomerForm(data=data)
        if form.is_valid():
            customer = form.save()
            self.assertEqual(customer.first_name, 'Jane')
            self.assertEqual(customer.last_name, 'Smith')
            self.assertEqual(customer.email, 'jane@example.com')


class TestDeviceForm(TestCase):
    """Test DeviceForm"""
    
    def setUp(self):
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
    
    def test_device_form_valid_data(self):
        """Test device form with valid data"""
        data = {
            'name': 'Test Device',
            'serial_number': 'SN001',
            'imei': '123456789012345',
            'customer': self.customer.uuid,
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = DeviceForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_device_form_save(self):
        """Test saving device form"""
        data = {
            'name': 'Test Phone',
            'serial_number': 'SN002',
            'imei': '987654321098765',
            'customer': self.customer.uuid,
            'organization': self.org.uuid,
            'branch': self.branch.uuid
        }
        form = DeviceForm(data=data)
        if form.is_valid():
            device = form.save()
            self.assertEqual(device.name, 'Test Phone')
            self.assertEqual(device.serial_number, 'SN002')


class TestCustomerTypeForm(TestCase):
    """Test CustomerTypeForm"""
    
    def test_customer_type_form_valid_data(self):
        """Test customer type form with valid data"""
        data = {
            'name': 'Retail',
            'code': 'RTL',
            'sequence': 1
        }
        form = CustomerTypeForm(data=data)
        self.assertTrue(form.is_valid())


class TestDeviceBrandForm(TestCase):
    """Test DeviceBrandForm"""
    
    def test_device_brand_form_valid_data(self):
        """Test device brand form with valid data"""
        data = {
            'name': 'Samsung',
            'code': 'SAM'
        }
        form = DeviceBrandForm(data=data)
        self.assertTrue(form.is_valid())
