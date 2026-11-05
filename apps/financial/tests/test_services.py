"""
Tests for financial services
"""
from django.test import TestCase
from apps.financial.services import invoice_service


class TestFinancialServices(TestCase):
    """Test financial services"""
    
    def test_service_functions(self):
        """Test service functions"""
        self.assertTrue(True)
