"""
API Views for Financial module
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    InvoiceStatus, InvoiceType, Invoice, InvoiceItem, InvoicePayment,
    Payment, PaymentMethod, Expense, ExpenseCategory, TaxRate,
    BudgetCategory, Budget, Currency
)
from .serializers import (
    InvoiceStatusSerializer, InvoiceTypeSerializer, InvoiceSerializer,
    InvoiceItemSerializer, InvoicePaymentSerializer, PaymentSerializer,
    PaymentMethodSerializer, ExpenseSerializer, ExpenseCategorySerializer,
    TaxRateSerializer, BudgetCategorySerializer, BudgetSerializer,
    CurrencySerializer
)
from apps.core.pagination import StandardResultsSetPagination


class InvoiceStatusViewSet(viewsets.ModelViewSet):
    queryset = InvoiceStatus.objects.all()
    serializer_class = InvoiceStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_default', 'is_final']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class InvoiceTypeViewSet(viewsets.ModelViewSet):
    queryset = InvoiceType.objects.all()
    serializer_class = InvoiceTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice_type', 'status', 'payment_status', 'customer', 'supplier', 'due_date', 'paid_date']
    search_fields = ['invoice_number', 'reference', 'customer__first_name', 'customer__last_name', 'supplier__name']
    ordering_fields = ['invoice_number', 'invoice_date', 'due_date', 'total_amount']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        invoice = self.get_object()
        items = invoice.items.all()
        serializer = InvoiceItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        invoice = self.get_object()
        payments = invoice.payments.all()
        serializer = InvoicePaymentSerializer(payments, many=True, context={'request': request})
        return Response(serializer.data)


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice', 'product', 'service', 'tax_rate']
    ordering_fields = ['quantity', 'unit_price', 'total']
    pagination_class = StandardResultsSetPagination


class InvoicePaymentViewSet(viewsets.ModelViewSet):
    queryset = InvoicePayment.objects.all()
    serializer_class = InvoicePaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice', 'payment_method', 'payment_date']
    ordering_fields = ['amount', 'payment_date', 'created_at']
    pagination_class = StandardResultsSetPagination


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_type', 'payment_method', 'status', 'customer', 'supplier', 'payment_date']
    search_fields = ['payment_number', 'reference', 'related_to']
    ordering_fields = ['payment_number', 'payment_date', 'amount']
    pagination_class = StandardResultsSetPagination


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'payment_method', 'supplier', 'expense_date', 'paid_date']
    search_fields = ['expense_number', 'title', 'description', 'supplier__name']
    ordering_fields = ['expense_number', 'expense_date', 'total_amount']
    pagination_class = StandardResultsSetPagination


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class TaxRateViewSet(viewsets.ModelViewSet):
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_default', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'rate']
    pagination_class = StandardResultsSetPagination


class BudgetCategoryViewSet(viewsets.ModelViewSet):
    queryset = BudgetCategory.objects.all()
    serializer_class = BudgetCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'period_start', 'period_end']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'period_start', 'allocated_amount']
    pagination_class = StandardResultsSetPagination


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_default']
    search_fields = ['code', 'name', 'symbol']
    ordering_fields = ['code', 'name']
    pagination_class = StandardResultsSetPagination
