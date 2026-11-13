"""
Serializers for Repair module
"""
from rest_framework import serializers
from .models import (
    RepairStatus, RepairPriority, RepairCategory, RepairType,
    RepairOrder, RepairOrderHistory, RepairPart, RepairService,
    RepairChecklist, RepairAttachment, RepairTemplate
)


class RepairStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairStatus
        fields = '__all__'


class RepairPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairPriority
        fields = '__all__'


class RepairCategorySerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = RepairCategory
        fields = '__all__'


class RepairTypeSerializer(serializers.ModelSerializer):
    category = RepairCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    
    class Meta:
        model = RepairType
        fields = '__all__'


class RepairOrderSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    device = serializers.CharField(source='device.name', read_only=True)
    device_id = serializers.UUIDField(source='device.uuid', write_only=True, required=False)
    status = RepairStatusSerializer(read_only=True)
    status_id = serializers.UUIDField(source='status.uuid', write_only=True, required=False)
    priority = RepairPrioritySerializer(read_only=True)
    priority_id = serializers.UUIDField(source='priority.uuid', write_only=True, required=False)
    category = RepairCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    type = RepairTypeSerializer(read_only=True)
    type_id = serializers.UUIDField(source='type.uuid', write_only=True, required=False)
    technician = serializers.CharField(source='technician.get_full_name', read_only=True)
    technician_id = serializers.UUIDField(source='technician.uuid', write_only=True, required=False)
    
    class Meta:
        model = RepairOrder
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'repair_number', 'total_cost')


class RepairOrderHistorySerializer(serializers.ModelSerializer):
    repair_order = serializers.CharField(source='repair_order.repair_number', read_only=True)
    repair_order_id = serializers.UUIDField(source='repair_order.uuid', write_only=True)
    performed_by = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    
    class Meta:
        model = RepairOrderHistory
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class RepairPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairPart
        fields = '__all__'


class RepairServiceSerializer(serializers.ModelSerializer):
    category = RepairCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    
    class Meta:
        model = RepairService
        fields = '__all__'


class RepairChecklistSerializer(serializers.ModelSerializer):
    repair_order = serializers.CharField(source='repair_order.repair_number', read_only=True)
    repair_order_id = serializers.UUIDField(source='repair_order.uuid', write_only=True)
    completed_by = serializers.CharField(source='completed_by.get_full_name', read_only=True)
    
    class Meta:
        model = RepairChecklist
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class RepairAttachmentSerializer(serializers.ModelSerializer):
    repair_order = serializers.CharField(source='repair_order.repair_number', read_only=True)
    repair_order_id = serializers.UUIDField(source='repair_order.uuid', write_only=True)
    uploaded_by = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = RepairAttachment
        fields = '__all__'
        read_only_fields = ('uuid', 'uploaded_at')


class RepairTemplateSerializer(serializers.ModelSerializer):
    category = RepairCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    
    class Meta:
        model = RepairTemplate
        fields = '__all__'
