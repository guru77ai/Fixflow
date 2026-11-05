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


class RepairStatusViewSet(viewsets.ModelViewSet):
    queryset = RepairStatus.objects.all()
    serializer_class = RepairStatusSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_default', 'is_final', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class RepairPriorityViewSet(viewsets.ModelViewSet):
    queryset = RepairPriority.objects.all()
    serializer_class = RepairPrioritySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'level', 'sequence']
    pagination_class = StandardResultsSetPagination


class RepairCategoryViewSet(viewsets.ModelViewSet):
    queryset = RepairCategory.objects.all()
    serializer_class = RepairCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination


class RepairTypeViewSet(viewsets.ModelViewSet):
    queryset = RepairType.objects.all()
    serializer_class = RepairTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'estimated_duration', 'base_price']
    pagination_class = StandardResultsSetPagination


class RepairOrderViewSet(viewsets.ModelViewSet):
    queryset = RepairOrder.objects.all()
    serializer_class = RepairOrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'type', 'technician', 'payment_status', 'is_warranty']
    search_fields = ['repair_number', 'customer__first_name', 'customer__last_name', 'device__name', 'device__serial_number', 'issue', 'diagnosis']
    ordering_fields = ['repair_number', 'received_date', 'completed_date', 'total_cost']
    pagination_class = StandardResultsSetPagination
    
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
        repair_order = self.get_object()
        new_status_id = request.data.get('status_id')
        if new_status_id:
            from .models import RepairStatus
            new_status = RepairStatus.objects.get(uuid=new_status_id)
            repair_order.status = new_status
            repair_order.save()
            
            # Create history record
            RepairOrderHistory.objects.create(
                repair_order=repair_order,
                action=f'Status changed to {new_status.name}',
                performed_by=request.user,
                notes=f'Status updated via API'
            )
            
            serializer = RepairOrderSerializer(repair_order, context={'request': request})
            return Response(serializer.data)
        return Response({'error': 'status_id is required'}, status=status.HTTP_400_BAD_REQUEST)


class RepairOrderHistoryViewSet(viewsets.ModelViewSet):
    queryset = RepairOrderHistory.objects.all()
    serializer_class = RepairOrderHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['repair_order', 'action', 'performed_by']
    search_fields = ['repair_order__repair_number', 'notes']
    ordering_fields = ['performed_at', 'created_at']
    pagination_class = StandardResultsSetPagination


class RepairPartViewSet(viewsets.ModelViewSet):
    queryset = RepairPart.objects.all()
    serializer_class = RepairPartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'part_number', 'description']
    ordering_fields = ['name', 'part_number', 'quantity', 'unit_cost']
    pagination_class = StandardResultsSetPagination


class RepairServiceViewSet(viewsets.ModelViewSet):
    queryset = RepairService.objects.all()
    serializer_class = RepairServiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'duration', 'price']
    pagination_class = StandardResultsSetPagination


class RepairChecklistViewSet(viewsets.ModelViewSet):
    queryset = RepairChecklist.objects.all()
    serializer_class = RepairChecklistSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['repair_order', 'is_complete', 'completed_by']
    search_fields = ['repair_order__repair_number', 'notes']
    ordering_fields = ['completed_at', 'created_at']
    pagination_class = StandardResultsSetPagination


class RepairAttachmentViewSet(viewsets.ModelViewSet):
    queryset = RepairAttachment.objects.all()
    serializer_class = RepairAttachmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['repair_order', 'file_type']
    search_fields = ['repair_order__repair_number', 'name', 'description']
    ordering_fields = ['uploaded_at', 'name']
    pagination_class = StandardResultsSetPagination


class RepairTemplateViewSet(viewsets.ModelViewSet):
    queryset = RepairTemplate.objects.all()
    serializer_class = RepairTemplateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'estimated_duration', 'base_price']
    pagination_class = StandardResultsSetPagination
