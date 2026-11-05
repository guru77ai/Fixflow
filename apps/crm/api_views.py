"""
API Views for CRM module
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Customer, Device, CustomerType, CustomerSource, CustomerGroup,
    DeviceBrand, DeviceModel, DeviceCategory, CustomerCommunication,
    CustomerDocument
)
from .serializers import (
    CustomerSerializer, DeviceSerializer, CustomerTypeSerializer,
    CustomerSourceSerializer, CustomerGroupSerializer, DeviceBrandSerializer,
    DeviceModelSerializer, DeviceCategorySerializer,
    CustomerCommunicationSerializer, CustomerDocumentSerializer
)
from apps.core.pagination import StandardResultsSetPagination


class CustomerTypeViewSet(viewsets.ModelViewSet):
    queryset = CustomerType.objects.all()
    serializer_class = CustomerTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class CustomerSourceViewSet(viewsets.ModelViewSet):
    queryset = CustomerSource.objects.all()
    serializer_class = CustomerSourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class CustomerGroupViewSet(viewsets.ModelViewSet):
    queryset = CustomerGroup.objects.all()
    serializer_class = CustomerGroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class DeviceCategoryViewSet(viewsets.ModelViewSet):
    queryset = DeviceCategory.objects.all()
    serializer_class = DeviceCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class DeviceBrandViewSet(viewsets.ModelViewSet):
    queryset = DeviceBrand.objects.all()
    serializer_class = DeviceBrandSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description', 'website']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class DeviceModelViewSet(viewsets.ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['brand', 'category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_vip', 'is_wholesale', 'customer_type', 'source', 'group']
    search_fields = ['customer_number', 'first_name', 'last_name', 'email', 'phone', 'tax_id']
    ordering_fields = ['customer_number', 'first_name', 'last_name', 'created_at']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        customer = self.get_object()
        data = {
            'total_devices': customer.devices.count(),
            'total_repairs': customer.repair_orders.count(),
            'total_invoices': customer.invoices.count(),
            'total_payments': customer.payments.count(),
            'total_spent': sum(invoice.total_amount or 0 for invoice in customer.invoices.all()),
            'balance': customer.balance or 0,
        }
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def devices(self, request, pk=None):
        customer = self.get_object()
        devices = customer.devices.all()
        serializer = DeviceSerializer(devices, many=True, context={'request': request})
        return Response(serializer.data)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'device_type', 'category', 'brand', 'model', 'warranty_status']
    search_fields = ['device_number', 'name', 'serial_number', 'imei', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['device_number', 'name', 'serial_number', 'created_at']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def repairs(self, request, pk=None):
        device = self.get_object()
        repairs = device.repair_orders.all()
        from apps.repair.serializers import RepairOrderSerializer
        serializer = RepairOrderSerializer(repairs, many=True, context={'request': request})
        return Response(serializer.data)


class CustomerCommunicationViewSet(viewsets.ModelViewSet):
    queryset = CustomerCommunication.objects.all()
    serializer_class = CustomerCommunicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'communication_type', 'communication_date']
    search_fields = ['customer__first_name', 'customer__last_name', 'subject', 'message']
    ordering_fields = ['communication_date', 'created_at']
    pagination_class = StandardResultsSetPagination


class CustomerDocumentViewSet(viewsets.ModelViewSet):
    queryset = CustomerDocument.objects.all()
    serializer_class = CustomerDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer', 'document_type', 'uploaded_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'name', 'description']
    ordering_fields = ['uploaded_at', 'name']
    pagination_class = StandardResultsSetPagination
