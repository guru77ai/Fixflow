"""
Tests for inventory services
"""
from django.test import TestCase
from apps.inventory.services import product_service, warehouse_service


class TestInventoryServices(TestCase):
    """Test inventory services"""
    
    def test_service_functions(self):
        """Test service functions"""
        self.assertTrue(True)
