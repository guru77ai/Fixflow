"""
Pagination classes for API views
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination with default page size of 20"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class SmallResultsSetPagination(PageNumberPagination):
    """Small pagination with default page size of 10"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class LargeResultsSetPagination(PageNumberPagination):
    """Large pagination with default page size of 50"""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
