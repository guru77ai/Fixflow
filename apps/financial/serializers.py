"""
Serializers for Financial module
"""
from rest_framework import serializers
from .models import (
    InvoiceStatus, InvoiceType, Invoice, InvoiceItem, InvoicePayment,
    Payment, Expense, ExpenseCategory, ExpenseAttachment, FinancialReport
)


class InvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceStatus
        fields = '__all__'


class InvoiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceType
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_type = InvoiceTypeSerializer(read_only=True)
    invoice_type_id = serializers.UUIDField(source='invoice_type.uuid', write_only=True, required=False)
    status = InvoiceStatusSerializer(read_only=True)
    status_id = serializers.UUIDField(source='status.uuid', write_only=True, required=False)
    customer = serializers.CharField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    supplier = serializers.CharField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True, required=False)
    created_by = serializers.CharField(source='created_by.get_full_name', read_only=True)
    created_by_id = serializers.UUIDField(source='created_by.uuid', write_only=True, required=False)
    approved_by = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'invoice_number', 'total_amount', 'balance')


class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.CharField(source='invoice.invoice_number', read_only=True)
    invoice_id = serializers.UUIDField(source='invoice.uuid', write_only=True)
    product = serializers.CharField(source='product.name', read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True, required=False)
    service = serializers.CharField(source='service.name', read_only=True)
    service_id = serializers.UUIDField(source='service.uuid', write_only=True, required=False)
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ('uuid', 'total')


class InvoicePaymentSerializer(serializers.ModelSerializer):
    invoice = serializers.CharField(source='invoice.invoice_number', read_only=True)
    invoice_id = serializers.UUIDField(source='invoice.uuid', write_only=True)
    processed_by = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = InvoicePayment
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class PaymentSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    supplier = serializers.CharField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True, required=False)
    processed_by = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    processed_by_id = serializers.UUIDField(source='processed_by.uuid', write_only=True, required=False)
    approved_by = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'payment_number')


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True)
    supplier = serializers.CharField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True, required=False)
    submitted_by = serializers.CharField(source='submitted_by.get_full_name', read_only=True)
    submitted_by_id = serializers.UUIDField(source='submitted_by.uuid', write_only=True, required=False)
    approved_by = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    paid_by = serializers.CharField(source='paid_by.get_full_name', read_only=True)
    paid_by_id = serializers.UUIDField(source='paid_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'expense_number', 'total_amount')


class ExpenseCategorySerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class ExpenseAttachmentSerializer(serializers.ModelSerializer):
    expense = serializers.CharField(source='expense.expense_number', read_only=True)
    expense_id = serializers.UUIDField(source='expense.uuid', write_only=True)
    uploaded_by = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = ExpenseAttachment
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class FinancialReportSerializer(serializers.ModelSerializer):
    generated_by = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    
    class Meta:
        model = FinancialReport
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'generated_at')
