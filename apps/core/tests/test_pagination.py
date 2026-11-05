"""
Tests for Core pagination classes
"""
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from apps.core.pagination import (
    StandardResultsSetPagination,
    SmallResultsSetPagination,
    LargeResultsSetPagination
)


class TestStandardResultsSetPagination(TestCase):
    """Test StandardResultsSetPagination class"""
    
    def setUp(self):
        self.paginator = StandardResultsSetPagination()
    
    def test_page_size(self):
        """Test that page size is 20"""
        self.assertEqual(self.paginator.page_size, 20)
    
    def test_page_size_query_param(self):
        """Test page size query parameter"""
        self.assertEqual(self.paginator.page_size_query_param, 'page_size')
    
    def test_max_page_size(self):
        """Test max page size"""
        self.assertEqual(self.paginator.max_page_size, 100)


class TestSmallResultsSetPagination(TestCase):
    """Test SmallResultsSetPagination class"""
    
    def setUp(self):
        self.paginator = SmallResultsSetPagination()
    
    def test_page_size(self):
        """Test that page size is 10"""
        self.assertEqual(self.paginator.page_size, 10)
    
    def test_max_page_size(self):
        """Test max page size"""
        self.assertEqual(self.paginator.max_page_size, 50)


class TestLargeResultsSetPagination(TestCase):
    """Test LargeResultsSetPagination class"""
    
    def setUp(self):
        self.paginator = LargeResultsSetPagination()
    
    def test_page_size(self):
        """Test that page size is 50"""
        self.assertEqual(self.paginator.page_size, 50)
    
    def test_max_page_size(self):
        """Test max page size"""
        self.assertEqual(self.paginator.max_page_size, 200)
