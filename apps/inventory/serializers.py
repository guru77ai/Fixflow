"""
Serializers for Inventory module
"""
from rest_framework import serializers
from .models import (
    Warehouse, ProductCategory, ProductBrand, UnitOfMeasure,
    Product, ProductSerialNumber, StockMovement, StockTransfer,
    StockTransferItem, StockAdjustment, StockAdjustmentItem,
    Service, ServiceCategory
)


class WarehouseSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(source='manager.get_full_name', read_only=True)
    manager_id = serializers.UUIDField(source='manager.uuid', write_only=True, required=False)
    
    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    brand = ProductBrandSerializer(read_only=True)
    brand_id = serializers.UUIDField(source='brand.uuid', write_only=True, required=False)
    uom = UnitOfMeasureSerializer(read_only=True)
    uom_id = serializers.UUIDField(source='uom.uuid', write_only=True, required=False)
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class ProductSerialNumberSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True)
    
    class Meta:
        model = ProductSerialNumber
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class StockMovementSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class StockTransferSerializer(serializers.ModelSerializer):
    from_warehouse = WarehouseSerializer(read_only=True)
    from_warehouse_id = serializers.UUIDField(source='from_warehouse.uuid', write_only=True)
    to_warehouse = WarehouseSerializer(read_only=True)
    to_warehouse_id = serializers.UUIDField(source='to_warehouse.uuid', write_only=True)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    received_by = serializers.CharField(source='received_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockTransfer
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'transfer_number')


class StockTransferItemSerializer(serializers.ModelSerializer):
    transfer = serializers.CharField(source='transfer.transfer_number', read_only=True)
    transfer_id = serializers.UUIDField(source='transfer.uuid', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True)
    
    class Meta:
        model = StockTransferItem
        fields = '__all__'
        read_only_fields = ('uuid',)


class StockAdjustmentSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.UUIDField(source='warehouse.uuid', write_only=True)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = StockAdjustment
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'adjustment_number')


class StockAdjustmentItemSerializer(serializers.ModelSerializer):
    adjustment = serializers.CharField(source='adjustment.adjustment_number', read_only=True)
    adjustment_id = serializers.UUIDField(source='adjustment.uuid', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True)
    
    class Meta:
        model = StockAdjustmentItem
        fields = '__all__'
        read_only_fields = ('uuid',)


class ServiceCategorySerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'service_number')
