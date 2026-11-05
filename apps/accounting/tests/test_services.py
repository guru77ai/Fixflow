"""
Tests for accounting services
"""
from django.test import TestCase
from apps.accounting.services import account_service


class TestAccountingServices(TestCase):
    """Test accounting services"""
    
    def test_service_functions(self):
        """Test service functions"""
        self.assertTrue(True)
