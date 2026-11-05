"""
Tests for CRM models
"""
import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.crm.models import (
    Customer, Device, CustomerType, CustomerSource, CustomerGroup,
    DeviceBrand, DeviceModel, DeviceCategory, CustomerCommunication,
    CustomerDocument
)

User = get_user_model()


@pytest.fixture
def create_customer_type():
    """Fixture to create a customer type"""
    return CustomerType.objects.create(
        name='Retail',
        code='RTL',
        description='Retail customer',
        sequence=1,
        is_active=True
    )


@pytest.fixture
def create_customer_source():
    """Fixture to create a customer source"""
    return CustomerSource.objects.create(
        name='Walk-in',
        code='WKIN',
        description='Walk-in customer',
        sequence=1,
        is_active=True
    )


@pytest.fixture
def create_customer_group():
    """Fixture to create a customer group"""
    return CustomerGroup.objects.create(
        name='Standard',
        code='STD',
        description='Standard group',
        is_active=True
    )


@pytest.fixture
def create_device_category():
    """Fixture to create a device category"""
    return DeviceCategory.objects.create(
        name='Smartphones',
        code='SMART',
        description='Smartphone devices',
        is_active=True
    )


@pytest.fixture
def create_device_brand():
    """Fixture to create a device brand"""
    return DeviceBrand.objects.create(
        name='Samsung',
        code='SAM',
        description='Samsung brand',
        website='https://www.samsung.com',
        is_active=True
    )


@pytest.fixture
def create_device_model(create_device_brand, create_device_category):
    """Fixture to create a device model"""
    return DeviceModel.objects.create(
        name='Galaxy S23',
        code='GS23',
        brand=create_device_brand,
        category=create_device_category,
        description='Samsung Galaxy S23',
        is_active=True
    )


@pytest.fixture
def create_customer(create_customer_type, create_customer_source, create_customer_group):
    """Fixture to create a customer"""
    return Customer.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@example.com',
        phone='1234567890',
        customer_type=create_customer_type,
        source=create_customer_source,
        group=create_customer_group,
        address='123 Main St',
        city='New York',
        state='NY',
        postal_code='10001',
        country='USA',
        status='active',
        is_vip=False,
        is_wholesale=False
    )


@pytest.fixture
def create_device(create_customer, create_device_brand, create_device_model, create_device_category):
    """Fixture to create a device"""
    return Device.objects.create(
        name='Johns Phone',
        device_type='Smartphone',
        customer=create_customer,
        category=create_device_category,
        brand=create_device_brand,
        model=create_device_model,
        serial_number='SN123456789',
        imei='IMEI123456789',
        color='Black',
        storage='256GB',
        os_version='Android 13',
        description='Samsung Galaxy S23',
        purchase_date='2023-01-01',
        warranty_status='active',
        warranty_expiry='2024-01-01',
        warranty_provider='Samsung',
        status='active'
    )


class TestCustomerType(TestCase):
    """Test CustomerType model"""
    
    def test_customer_type_creation(self):
        """Test creating a customer type"""
        customer_type = CustomerType.objects.create(
            name='Wholesale',
            code='WSL',
            description='Wholesale customer',
            sequence=2,
            is_active=True
        )
        self.assertEqual(customer_type.name, 'Wholesale')
        self.assertEqual(customer_type.code, 'WSL')
        self.assertTrue(customer_type.is_active)
    
    def test_customer_type_str(self):
        """Test string representation of customer type"""
        customer_type = CustomerType.objects.create(
            name='Retail',
            code='RTL'
        )
        self.assertEqual(str(customer_type), 'Retail')


class TestCustomerSource(TestCase):
    """Test CustomerSource model"""
    
    def test_customer_source_creation(self):
        """Test creating a customer source"""
        source = CustomerSource.objects.create(
            name='Online',
            code='ONL',
            description='Online customer',
            sequence=2,
            is_active=True
        )
        self.assertEqual(source.name, 'Online')
        self.assertEqual(source.code, 'ONL')


class TestCustomerGroup(TestCase):
    """Test CustomerGroup model"""
    
    def test_customer_group_creation(self):
        """Test creating a customer group"""
        group = CustomerGroup.objects.create(
            name='Premium',
            code='PREM',
            description='Premium group'
        )
        self.assertEqual(group.name, 'Premium')


class TestDeviceCategory(TestCase):
    """Test DeviceCategory model"""
    
    def test_device_category_creation(self):
        """Test creating a device category"""
        category = DeviceCategory.objects.create(
            name='Laptops',
            code='LAP',
            description='Laptop devices'
        )
        self.assertEqual(category.name, 'Laptops')


class TestDeviceBrand(TestCase):
    """Test DeviceBrand model"""
    
    def test_device_brand_creation(self):
        """Test creating a device brand"""
        brand = DeviceBrand.objects.create(
            name='Apple',
            code='APP',
            website='https://www.apple.com'
        )
        self.assertEqual(brand.name, 'Apple')


class TestDeviceModel(TestCase):
    """Test DeviceModel model"""
    
    def test_device_model_creation(self):
        """Test creating a device model"""
        brand = DeviceBrand.objects.create(name='Apple', code='APP')
        category = DeviceCategory.objects.create(name='Phones', code='PHN')
        model = DeviceModel.objects.create(
            name='iPhone 15',
            code='IP15',
            brand=brand,
            category=category
        )
        self.assertEqual(model.name, 'iPhone 15')
        self.assertEqual(model.brand.name, 'Apple')


class TestCustomer(TestCase):
    """Test Customer model"""
    
    def test_customer_creation(self):
        """Test creating a customer"""
        customer_type = CustomerType.objects.create(name='Retail', code='RTL')
        customer = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com',
            phone='9876543210',
            customer_type=customer_type,
            status='active'
        )
        self.assertEqual(customer.full_name, 'Jane Smith')
        self.assertEqual(customer.email, 'jane.smith@example.com')
        self.assertEqual(customer.status, 'active')
    
    def test_customer_str(self):
        """Test string representation of customer"""
        customer = Customer.objects.create(
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@example.com'
        )
        self.assertEqual(str(customer), 'Jane Smith')


class TestDevice(TestCase):
    """Test Device model"""
    
    def test_device_creation(self):
        """Test creating a device"""
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        device = Device.objects.create(
            name='My Phone',
            device_type='Smartphone',
            customer=customer,
            serial_number='SN123',
            status='active'
        )
        self.assertEqual(device.name, 'My Phone')
        self.assertEqual(device.customer.full_name, 'John Doe')
    
    def test_device_str(self):
        """Test string representation of device"""
        device = Device.objects.create(
            name='My Phone',
            device_type='Smartphone',
            serial_number='SN123'
        )
        self.assertEqual(str(device), 'My Phone')


class TestCustomerCommunication(TestCase):
    """Test CustomerCommunication model"""
    
    def test_communication_creation(self):
        """Test creating a customer communication"""
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        communication = CustomerCommunication.objects.create(
            customer=customer,
            communication_type='email',
            subject='Test Email',
            message='This is a test message'
        )
        self.assertEqual(communication.subject, 'Test Email')


class TestCustomerDocument(TestCase):
    """Test CustomerDocument model"""
    
    def test_document_creation(self):
        """Test creating a customer document"""
        customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        document = CustomerDocument.objects.create(
            customer=customer,
            name='ID Proof',
            document_type='id_proof',
            description='Customer ID proof'
        )
        self.assertEqual(document.name, 'ID Proof')
