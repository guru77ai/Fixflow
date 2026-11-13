"""
Serializers for CRM module
"""
from rest_framework import serializers
from .models import (
    Customer, Device, CustomerType, CustomerSource, CustomerGroup,
    DeviceBrand, DeviceModel, DeviceCategory, CustomerCommunication,
    CustomerDocument
)


class CustomerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerType
        fields = '__all__'


class CustomerSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSource
        fields = '__all__'


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = '__all__'


class DeviceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceCategory
        fields = '__all__'


class DeviceBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceBrand
        fields = '__all__'


class DeviceModelSerializer(serializers.ModelSerializer):
    brand = DeviceBrandSerializer(read_only=True)
    brand_id = serializers.UUIDField(source='brand.uuid', write_only=True, required=False)
    
    class Meta:
        model = DeviceModel
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    customer_type = CustomerTypeSerializer(read_only=True)
    customer_type_id = serializers.UUIDField(source='customer_type.uuid', write_only=True, required=False)
    source = CustomerSourceSerializer(read_only=True)
    source_id = serializers.UUIDField(source='source.uuid', write_only=True, required=False)
    group = CustomerGroupSerializer(read_only=True)
    group_id = serializers.UUIDField(source='group.uuid', write_only=True, required=False)
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'customer_number')


class DeviceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    category = DeviceCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    brand = DeviceBrandSerializer(read_only=True)
    brand_id = serializers.UUIDField(source='brand.uuid', write_only=True, required=False)
    model = DeviceModelSerializer(read_only=True)
    model_id = serializers.UUIDField(source='model.uuid', write_only=True, required=False)
    
    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'device_number')


class CustomerCommunicationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = CustomerCommunication
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class CustomerDocumentSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True)
    uploaded_by = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = CustomerDocument
        fields = '__all__'
        read_only_fields = ('uuid', 'uploaded_at')
