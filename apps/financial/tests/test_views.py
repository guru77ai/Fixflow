"""
Tests for Financial views
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.core.models import Organization, Branch
from apps.financial.models import InvoiceStatus, InvoiceType

User = get_user_model()


class TestInvoiceStatusViews(TestCase):
    """Test InvoiceStatus views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.invoice_status = InvoiceStatus.objects.create(
            name='Draft',
            code='draft',
            description='Invoice is being prepared',
            color='#999999',
            sequence=1
        )
    
    def test_invoice_status_list_view(self):
        """Test invoice status list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('financial:invoice_status_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invoice Statuses')


class TestInvoiceTypeViews(TestCase):
    """Test InvoiceType views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.invoice_type = InvoiceType.objects.create(
            name='Repair Invoice',
            code='REPAIR',
            description='Invoice for repair services',
            prefix='REP-INV',
            is_active=True
        )
    
    def test_invoice_type_list_view(self):
        """Test invoice type list view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('financial:invoice_type_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invoice Types')
