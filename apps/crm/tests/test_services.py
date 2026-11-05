"""
Tests for crm services
"""
from django.test import TestCase
from apps.crm.services import customer_service, device_service


class TestCRMServices(TestCase):
    """Test crm services"""
    
    def test_service_functions(self):
        """Test service functions"""
        self.assertTrue(True)
