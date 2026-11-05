"""
API Views for POS module
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    PaymentMethod, CashRegister, Sale, SaleItem, SalePayment,
    Receipt, Refund, RefundItem, POSSession, POSSettings
)
from .serializers import (
    PaymentMethodSerializer, CashRegisterSerializer, SaleSerializer,
    SaleItemSerializer, SalePaymentSerializer, ReceiptSerializer,
    RefundSerializer, RefundItemSerializer, POSSessionSerializer,
    POSSettingsSerializer
)
from apps.core.pagination import StandardResultsSetPagination


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class CashRegisterViewSet(viewsets.ModelViewSet):
    queryset = CashRegister.objects.all()
    serializer_class = CashRegisterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'current_balance']
    pagination_class = StandardResultsSetPagination


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'sale_type', 'customer', 'cash_register', 'sale_date']
    search_fields = ['sale_number', 'customer__first_name', 'customer__last_name', 'notes']
    ordering_fields = ['sale_number', 'sale_date', 'total_amount']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        sale = self.get_object()
        items = sale.items.all()
        serializer = SaleItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payments(self, request, pk=None):
        sale = self.get_object()
        payments = sale.payments.all()
        serializer = SalePaymentSerializer(payments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def receipt(self, request, pk=None):
        sale = self.get_object()
        try:
            receipt = sale.receipt
            serializer = ReceiptSerializer(receipt, context={'request': request})
            return Response(serializer.data)
        except Receipt.DoesNotExist:
            return Response({'error': 'No receipt found for this sale'}, status=404)


class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sale', 'product', 'service']
    ordering_fields = ['quantity', 'unit_price', 'total_price']
    pagination_class = StandardResultsSetPagination


class SalePaymentViewSet(viewsets.ModelViewSet):
    queryset = SalePayment.objects.all()
    serializer_class = SalePaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sale', 'payment_method', 'payment_date']
    ordering_fields = ['amount', 'payment_date', 'created_at']
    pagination_class = StandardResultsSetPagination


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sale', 'receipt_type', 'email_sent']
    search_fields = ['receipt_number', 'sale__sale_number']
    ordering_fields = ['receipt_number', 'uploaded_at', 'created_at']
    pagination_class = StandardResultsSetPagination


class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'refund_type', 'sale', 'customer', 'refund_date']
    search_fields = ['refund_number', 'sale__sale_number', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['refund_number', 'refund_date', 'total_amount']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        refund = self.get_object()
        items = refund.items.all()
        serializer = RefundItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)


class RefundItemViewSet(viewsets.ModelViewSet):
    queryset = RefundItem.objects.all()
    serializer_class = RefundItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['refund', 'sale_item', 'product']
    ordering_fields = ['quantity', 'unit_price', 'total_price']
    pagination_class = StandardResultsSetPagination


class POSSessionViewSet(viewsets.ModelViewSet):
    queryset = POSSession.objects.all()
    serializer_class = POSSessionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cash_register', 'user', 'status', 'start_time', 'end_time']
    search_fields = ['session_number']
    ordering_fields = ['session_number', 'start_time', 'end_time']
    pagination_class = StandardResultsSetPagination


class POSSettingsViewSet(viewsets.ModelViewSet):
    queryset = POSSettings.objects.all()
    serializer_class = POSSettingsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['default_receipt_type', 'auto_print_receipt']
    pagination_class = StandardResultsSetPagination
