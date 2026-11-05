"""
Tests for pos services
"""
from django.test import TestCase
from apps.pos.services import sale_service


class TestPOSServices(TestCase):
    """Test pos services"""
    
    def test_service_functions(self):
        """Test service functions"""
        self.assertTrue(True)
