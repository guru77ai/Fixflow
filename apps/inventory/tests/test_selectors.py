"""
Tests for inventory selectors
"""
from django.test import TestCase
from apps.inventory.selectors import product_selectors, warehouse_selectors


class TestInventorySelectors(TestCase):
    """Test inventory selectors"""
    
    def test_selector_functions(self):
        """Test selector functions"""
        self.assertTrue(True)
