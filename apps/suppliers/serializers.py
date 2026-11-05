"""
Serializers for Suppliers module
"""
from rest_framework import serializers
from .models import SupplierCategory, Supplier, SupplierContact, SupplierDocument


class SupplierCategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = SupplierCategory
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    category = SupplierCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True, required=False)
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'supplier_number')


class SupplierContactSerializer(serializers.ModelSerializer):
    supplier = serializers.StringField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True)
    
    class Meta:
        model = SupplierContact
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class SupplierDocumentSerializer(serializers.ModelSerializer):
    supplier = serializers.StringField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True)
    uploaded_by = serializers.StringField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = SupplierDocument
        fields = '__all__'
        read_only_fields = ('uuid', 'uploaded_at')
