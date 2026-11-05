"""
Serializers for POS module
"""
from rest_framework import serializers
from .models import (
    PaymentMethod, CashRegister, Sale, SaleItem, SalePayment,
    Receipt, Refund, RefundItem, POSSession, POSSettings
)


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegister
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class SaleSerializer(serializers.ModelSerializer):
    customer = serializers.StringField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    cash_register = serializers.StringField(source='cash_register.name', read_only=True)
    cash_register_id = serializers.UUIDField(source='cash_register.uuid', write_only=True, required=False)
    technician = serializers.StringField(source='technician.get_full_name', read_only=True)
    technician_id = serializers.UUIDField(source='technician.uuid', write_only=True, required=False)
    
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'sale_number', 'total_amount')


class SaleItemSerializer(serializers.ModelSerializer):
    sale = serializers.StringField(source='sale.sale_number', read_only=True)
    sale_id = serializers.UUIDField(source='sale.uuid', write_only=True)
    product = serializers.StringField(source='product.name', read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True, required=False)
    service = serializers.StringField(source='service.name', read_only=True)
    service_id = serializers.UUIDField(source='service.uuid', write_only=True, required=False)
    
    class Meta:
        model = SaleItem
        fields = '__all__'
        read_only_fields = ('uuid',)


class SalePaymentSerializer(serializers.ModelSerializer):
    sale = serializers.StringField(source='sale.sale_number', read_only=True)
    sale_id = serializers.UUIDField(source='sale.uuid', write_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_method_id = serializers.UUIDField(source='payment_method.uuid', write_only=True)
    processed_by = serializers.StringField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = SalePayment
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class ReceiptSerializer(serializers.ModelSerializer):
    sale = serializers.StringField(source='sale.sale_number', read_only=True)
    sale_id = serializers.UUIDField(source='sale.uuid', write_only=True)
    customer = serializers.StringField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    created_by = serializers.StringField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class RefundSerializer(serializers.ModelSerializer):
    sale = serializers.StringField(source='sale.sale_number', read_only=True)
    sale_id = serializers.UUIDField(source='sale.uuid', write_only=True)
    customer = serializers.StringField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    processed_by = serializers.StringField(source='processed_by.get_full_name', read_only=True)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = Refund
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'refund_number')


class RefundItemSerializer(serializers.ModelSerializer):
    refund = serializers.StringField(source='refund.refund_number', read_only=True)
    refund_id = serializers.UUIDField(source='refund.uuid', write_only=True)
    sale_item = serializers.StringField(source='sale_item.pk', read_only=True)
    sale_item_id = serializers.UUIDField(source='sale_item.uuid', write_only=True, required=False)
    product = serializers.StringField(source='product.name', read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True, required=False)
    
    class Meta:
        model = RefundItem
        fields = '__all__'
        read_only_fields = ('uuid',)


class POSSessionSerializer(serializers.ModelSerializer):
    cash_register = CashRegisterSerializer(read_only=True)
    cash_register_id = serializers.UUIDField(source='cash_register.uuid', write_only=True)
    user = serializers.StringField(source='user.get_full_name', read_only=True)
    user_id = serializers.UUIDField(source='user.uuid', write_only=True)
    
    class Meta:
        model = POSSession
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'session_number')


class POSSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = POSSettings
        fields = '__all__'
        read_only_fields = ('uuid',)
