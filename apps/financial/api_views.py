"""
API Views for Financial module
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    InvoiceStatus, InvoiceType, Invoice, InvoiceItem, InvoicePayment,
    Payment, Expense, ExpenseCategory, ExpenseAttachment, FinancialReport
)
from .serializers import (
    InvoiceStatusSerializer, InvoiceTypeSerializer, InvoiceSerializer,
    InvoiceItemSerializer, InvoicePaymentSerializer, PaymentSerializer,
    ExpenseSerializer, ExpenseCategorySerializer,
    ExpenseAttachmentSerializer, FinancialReportSerializer
)
from apps.core.pagination import StandardResultsSetPagination
from apps.core.api_mixins import TenantScopedMixin


class InvoiceStatusViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = InvoiceStatus.objects.all()
    serializer_class = InvoiceStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_default', 'is_final']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class InvoiceTypeViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = InvoiceType.objects.all()
    serializer_class = InvoiceTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination


class InvoiceViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice_type', 'status', 'customer', 'supplier', 'payment_status']
    search_fields = ['invoice_number', 'reference', 'customer__first_name', 'customer__last_name', 'supplier__name']
    ordering_fields = ['invoice_number', 'created_at', 'due_date', 'total_amount']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class InvoiceItemViewSet(viewsets.ModelViewSet):
    """Child items - scoped through parent Invoice"""
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice']
    search_fields = ['description', 'invoice__invoice_number']
    ordering_fields = ['invoice', 'product', 'service']
    pagination_class = StandardResultsSetPagination


class InvoicePaymentViewSet(viewsets.ModelViewSet):
    """Child items - scoped through parent Invoice"""
    queryset = InvoicePayment.objects.all()
    serializer_class = InvoicePaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice']
    search_fields = ['invoice__invoice_number', 'reference']
    ordering_fields = ['invoice', 'payment_date', 'amount']
    pagination_class = StandardResultsSetPagination


class PaymentViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_type', 'status', 'customer', 'supplier']
    search_fields = ['payment_number', 'reference', 'customer__first_name', 'customer__last_name', 'supplier__name']
    ordering_fields = ['payment_number', 'payment_date', 'amount']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class ExpenseCategoryViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class ExpenseViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'supplier']
    search_fields = ['expense_number', 'title', 'description', 'supplier__name']
    ordering_fields = ['expense_number', 'expense_date', 'amount']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class ExpenseAttachmentViewSet(viewsets.ModelViewSet):
    """Child items - scoped through parent Expense"""
    queryset = ExpenseAttachment.objects.all()
    serializer_class = ExpenseAttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['expense']
    search_fields = ['expense__expense_number', 'title', 'description']
    ordering_fields = ['expense', 'created_at']
    pagination_class = StandardResultsSetPagination


class FinancialReportViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'generated_by']
    search_fields = ['name', 'report_type']
    ordering_fields = ['name', 'start_date', 'end_date', 'generated_at']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
