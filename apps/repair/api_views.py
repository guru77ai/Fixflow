"""
API Views for Repair module
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    RepairStatus, RepairPriority, RepairCategory, RepairType,
    RepairOrder, RepairOrderHistory, RepairPart, RepairService,
    RepairChecklist, RepairAttachment, RepairTemplate
)
from .serializers import (
    RepairStatusSerializer, RepairPrioritySerializer, RepairCategorySerializer,
    RepairTypeSerializer, RepairOrderSerializer, RepairOrderHistorySerializer,
    RepairPartSerializer, RepairServiceSerializer, RepairChecklistSerializer,
    RepairAttachmentSerializer, RepairTemplateSerializer
)
from apps.core.pagination import StandardResultsSetPagination
from apps.core.api_mixins import TenantScopedMixin


class RepairStatusViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairStatus.objects.all()
    serializer_class = RepairStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_default', 'is_final', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class RepairPriorityViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairPriority.objects.all()
    serializer_class = RepairPrioritySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'level', 'sequence']
    pagination_class = StandardResultsSetPagination


class RepairCategoryViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairCategory.objects.all()
    serializer_class = RepairCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class RepairTypeViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairType.objects.all()
    serializer_class = RepairTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'estimated_duration', 'base_price']
    pagination_class = StandardResultsSetPagination


class RepairOrderViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'type', 'technician', 'payment_status', 'is_warranty']
    search_fields = ['repair_number', 'customer__first_name', 'customer__last_name', 'device__name', 'device__serial_number', 'issue', 'diagnosis']
    ordering_fields = ['repair_number', 'received_date', 'completed_date', 'total_cost']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        repair_order = self.get_object()
        history = repair_order.history.all()
        serializer = RepairOrderHistorySerializer(history, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def parts(self, request, pk=None):
        repair_order = self.get_object()
        parts = repair_order.parts.all()
        serializer = RepairPartSerializer(parts, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        repair_order = self.get_object()
        services = repair_order.services.all()
        serializer = RepairServiceSerializer(services, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attachments(self, request, pk=None):
        repair_order = self.get_object()
        attachments = repair_order.attachments.all()
        serializer = RepairAttachmentSerializer(attachments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update repair order status with validation.
        
        Validates:
        - Repair order belongs to current tenant
        - New status exists and is valid
        - Status transition is allowed (if business rules exist)
        - User has permission to change status
        """
        from .models import RepairStatus, RepairOrderHistory
        from rest_framework.exceptions import ValidationError, PermissionDenied
        from .services import RepairOrderService
        
        repair_order = self.get_object()
        self.validate_tenant(repair_order)
        
        new_status_id = request.data.get('status_id')
        if not new_status_id:
            return Response({'error': 'status_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            new_status = RepairStatus.objects.get(uuid=new_status_id)
        except RepairStatus.DoesNotExist:
            raise ValidationError({'error': 'Invalid status ID'})
        
        # Validate status transition using domain service
        try:
            updated_order = RepairOrderService.update_status(
                repair_order=repair_order,
                new_status=new_status,
                changed_by=request.user,
                notes=request.data.get('notes', 'Status updated via API')
            )
        except PermissionDenied as e:
            raise PermissionDenied(str(e))
        except ValidationError as e:
            raise ValidationError(str(e))
        
        serializer = RepairOrderSerializer(updated_order, context={'request': request})
        return Response(serializer.data)


class RepairOrderHistoryViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairOrderHistory.objects.all()
    serializer_class = RepairOrderHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['repair_order', 'action', 'performed_by']
    search_fields = ['repair_order__repair_number', 'notes']
    ordering_fields = ['performed_at', 'created_at']
    pagination_class = StandardResultsSetPagination


class RepairPartViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairPart.objects.all()
    serializer_class = RepairPartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'part_number', 'description']
    ordering_fields = ['name', 'part_number', 'quantity', 'unit_cost']
    pagination_class = StandardResultsSetPagination


class RepairServiceViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairService.objects.all()
    serializer_class = RepairServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'duration', 'price']
    pagination_class = StandardResultsSetPagination


class RepairChecklistViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairChecklist.objects.all()
    serializer_class = RepairChecklistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['repair_order', 'is_complete', 'completed_by']
    search_fields = ['repair_order__repair_number', 'notes']
    ordering_fields = ['completed_at', 'created_at']
    pagination_class = StandardResultsSetPagination


class RepairAttachmentViewSet(viewsets.ModelViewSet):
    """Global reference data - no tenant scoping needed"""
    queryset = RepairAttachment.objects.all()
    serializer_class = RepairAttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['repair_order', 'file_type']
    search_fields = ['repair_order__repair_number', 'name', 'description']
    ordering_fields = ['uploaded_at', 'name']
    pagination_class = StandardResultsSetPagination


class RepairTemplateViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = RepairTemplate.objects.all()
    serializer_class = RepairTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'estimated_duration', 'base_price']
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
