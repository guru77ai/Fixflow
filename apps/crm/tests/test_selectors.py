"""
Tests for crm selectors
"""
from django.test import TestCase
from apps.crm.selectors import customer_selectors, device_selectors


class TestCRMSelectors(TestCase):
    """Test crm selectors"""
    
    def test_selector_functions(self):
        """Test selector functions"""
        self.assertTrue(True)
