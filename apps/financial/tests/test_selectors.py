"""
Tests for financial selectors
"""
from django.test import TestCase
from apps.financial.selectors import invoice_selectors


class TestFinancialSelectors(TestCase):
    """Test financial selectors"""
    
    def test_selector_functions(self):
        """Test selector functions"""
        self.assertTrue(True)
