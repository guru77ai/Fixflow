"""
API Views for Inventory module
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Warehouse, ProductCategory, ProductBrand, UnitOfMeasure,
    Product, ProductSerialNumber, StockMovement, StockTransfer,
    StockTransferItem, StockAdjustment, StockAdjustmentItem,
    Service, ServiceCategory
)
from .serializers import (
    WarehouseSerializer, ProductCategorySerializer, ProductBrandSerializer,
    UnitOfMeasureSerializer, ProductSerializer, ProductSerialNumberSerializer,
    StockMovementSerializer, StockTransferSerializer, StockTransferItemSerializer,
    StockAdjustmentSerializer, StockAdjustmentItemSerializer,
    ServiceSerializer, ServiceCategorySerializer
)
from apps.core.pagination import StandardResultsSetPagination


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'organization', 'branch']
    search_fields = ['name', 'code', 'location', 'manager__first_name', 'manager__last_name']
    ordering_fields = ['name', 'code', 'location']
    pagination_class = StandardResultsSetPagination


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active', 'organization', 'branch']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class ProductBrandViewSet(viewsets.ModelViewSet):
    queryset = ProductBrand.objects.all()
    serializer_class = ProductBrandSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description', 'website']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination


class UnitOfMeasureViewSet(viewsets.ModelViewSet):
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'symbol']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'brand', 'uom', 'is_active', 'is_serialized', 'is_service']
    search_fields = ['sku', 'name', 'barcode', 'description']
    ordering_fields = ['sku', 'name', 'unit_cost', 'selling_price', 'current_stock']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def stock(self, request, pk=None):
        product = self.get_object()
        data = {
            'current_stock': product.current_stock,
            'minimum_stock': product.minimum_stock,
            'maximum_stock': product.maximum_stock,
            'is_below_minimum': product.current_stock < product.minimum_stock,
            'stock_movements': StockMovementSerializer(
                product.stock_movements.all().order_by('-date')[:10],
                many=True,
                context={'request': request}
            ).data
        }
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def serial_numbers(self, request, pk=None):
        product = self.get_object()
        serial_numbers = product.serial_numbers.all()
        serializer = ProductSerialNumberSerializer(serial_numbers, many=True, context={'request': request})
        return Response(serializer.data)


class ProductSerialNumberViewSet(viewsets.ModelViewSet):
    queryset = ProductSerialNumber.objects.all()
    serializer_class = ProductSerialNumberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'status', 'purchase_date', 'warranty_expiry']
    search_fields = ['serial_number', 'product__name', 'product__sku']
    ordering_fields = ['serial_number', 'purchase_date', 'warranty_expiry']
    pagination_class = StandardResultsSetPagination


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'movement_type', 'date']
    search_fields = ['product__name', 'product__sku', 'reference', 'notes']
    ordering_fields = ['date', 'created_at']
    pagination_class = StandardResultsSetPagination


class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.all()
    serializer_class = StockTransferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'from_warehouse', 'to_warehouse', 'transfer_date']
    search_fields = ['transfer_number', 'notes']
    ordering_fields = ['transfer_number', 'transfer_date', 'created_at']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        transfer = self.get_object()
        items = transfer.items.all()
        serializer = StockTransferItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)


class StockTransferItemViewSet(viewsets.ModelViewSet):
    queryset = StockTransferItem.objects.all()
    serializer_class = StockTransferItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['transfer', 'product']
    ordering_fields = ['quantity']
    pagination_class = StandardResultsSetPagination


class StockAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustment.objects.all()
    serializer_class = StockAdjustmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['adjustment_type', 'status', 'warehouse', 'adjustment_date']
    search_fields = ['adjustment_number', 'notes']
    ordering_fields = ['adjustment_number', 'adjustment_date', 'created_at']
    pagination_class = StandardResultsSetPagination
    
    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        adjustment = self.get_object()
        items = adjustment.items.all()
        serializer = StockAdjustmentItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data)


class StockAdjustmentItemViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustmentItem.objects.all()
    serializer_class = StockAdjustmentItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['adjustment', 'product']
    ordering_fields = ['quantity']
    pagination_class = StandardResultsSetPagination


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active', 'organization', 'branch']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['service_number', 'name', 'description']
    ordering_fields = ['service_number', 'name', 'duration', 'price']
    pagination_class = StandardResultsSetPagination
