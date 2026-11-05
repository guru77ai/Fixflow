"""
API Views for Suppliers module
"""
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import SupplierCategory, Supplier, SupplierContact, SupplierDocument
from .serializers import (
    SupplierCategorySerializer, SupplierSerializer,
    SupplierContactSerializer, SupplierDocumentSerializer
)
from apps.core.pagination import StandardResultsSetPagination


class SupplierCategoryViewSet(viewsets.ModelViewSet):
    queryset = SupplierCategory.objects.all()
    serializer_class = SupplierCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_active']
    search_fields = ['supplier_number', 'name', 'email', 'phone', 'tax_id', 'website']
    ordering_fields = ['supplier_number', 'name', 'created_at']
    pagination_class = StandardResultsSetPagination


class SupplierContactViewSet(viewsets.ModelViewSet):
    queryset = SupplierContact.objects.all()
    serializer_class = SupplierContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier', 'position', 'is_primary']
    search_fields = ['supplier__name', 'first_name', 'last_name', 'email', 'phone']
    ordering_fields = ['first_name', 'last_name', 'created_at']
    pagination_class = StandardResultsSetPagination


class SupplierDocumentViewSet(viewsets.ModelViewSet):
    queryset = SupplierDocument.objects.all()
    serializer_class = SupplierDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['supplier', 'document_type']
    search_fields = ['supplier__name', 'name', 'description']
    ordering_fields = ['uploaded_at', 'name']
    pagination_class = StandardResultsSetPagination
