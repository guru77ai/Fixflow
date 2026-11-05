"""
Tests for CRM views
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.crm.models import Customer, CustomerType

User = get_user_model()


@pytest.fixture
def client():
    """Fixture to create a test client"""
    return Client()


@pytest.fixture
def user():
    """Fixture to create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(client, user):
    """Fixture to create an authenticated client"""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.fixture
def customer_type():
    """Fixture to create a customer type"""
    return CustomerType.objects.create(
        name='Retail',
        code='RTL',
        is_active=True
    )


@pytest.fixture
def customer(customer_type):
    """Fixture to create a customer"""
    return Customer.objects.create(
        first_name='John',
        last_name='Doe',
        email='john@example.com',
        phone='1234567890',
        customer_type=customer_type,
        status='active'
    )


class TestCustomerListView(TestCase):
    """Test CustomerListView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer_type = CustomerType.objects.create(
            name='Retail',
            code='RTL',
            is_active=True
        )
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            customer_type=self.customer_type,
            status='active'
        )
    
    def test_customer_list_view_requires_login(self):
        """Test that customer list view requires login"""
        response = self.client.get(reverse('crm:customer_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_list_view_with_authentication(self):
        """Test customer list view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('crm:customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')


class TestCustomerDetailView(TestCase):
    """Test CustomerDetailView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer_type = CustomerType.objects.create(
            name='Retail',
            code='RTL',
            is_active=True
        )
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            customer_type=self.customer_type,
            status='active'
        )
    
    def test_customer_detail_view_requires_login(self):
        """Test that customer detail view requires login"""
        response = self.client.get(reverse('crm:customer_detail', args=[self.customer.uuid]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_detail_view_with_authentication(self):
        """Test customer detail view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('crm:customer_detail', args=[self.customer.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')


class TestCustomerCreateView(TestCase):
    """Test CustomerCreateView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer_type = CustomerType.objects.create(
            name='Retail',
            code='RTL',
            is_active=True
        )
    
    def test_customer_create_view_requires_login(self):
        """Test that customer create view requires login"""
        response = self.client.get(reverse('crm:customer_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_create_view_with_authentication(self):
        """Test customer create view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('crm:customer_create'))
        self.assertEqual(response.status_code, 200)


class TestCustomerUpdateView(TestCase):
    """Test CustomerUpdateView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer_type = CustomerType.objects.create(
            name='Retail',
            code='RTL',
            is_active=True
        )
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            customer_type=self.customer_type,
            status='active'
        )
    
    def test_customer_update_view_requires_login(self):
        """Test that customer update view requires login"""
        response = self.client.get(reverse('crm:customer_edit', args=[self.customer.uuid]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_update_view_with_authentication(self):
        """Test customer update view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('crm:customer_edit', args=[self.customer.uuid]))
        self.assertEqual(response.status_code, 200)


class TestCustomerDeleteView(TestCase):
    """Test CustomerDeleteView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.customer_type = CustomerType.objects.create(
            name='Retail',
            code='RTL',
            is_active=True
        )
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            customer_type=self.customer_type,
            status='active'
        )
    
    def test_customer_delete_view_requires_login(self):
        """Test that customer delete view requires login"""
        response = self.client.get(reverse('crm:customer_delete', args=[self.customer.uuid]))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_delete_view_with_authentication(self):
        """Test customer delete view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('crm:customer_delete', args=[self.customer.uuid]))
        self.assertEqual(response.status_code, 200)
