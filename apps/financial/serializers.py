"""
Serializers for Financial module
"""
from rest_framework import serializers
from .models import (
    InvoiceStatus, InvoiceType, Invoice, InvoiceItem, InvoicePayment,
    Payment, PaymentMethod, Expense, ExpenseCategory, TaxRate,
    BudgetCategory, Budget, Currency
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
    customer = serializers.StringField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    supplier = serializers.StringField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True, required=False)
    payment_method = serializers.StringField(source='payment_method.name', read_only=True)
    payment_method_id = serializers.UUIDField(source='payment_method.uuid', write_only=True, required=False)
    created_by = serializers.StringField(source='created_by.get_full_name', read_only=True)
    created_by_id = serializers.UUIDField(source='created_by.uuid', write_only=True, required=False)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'invoice_number', 'total_amount', 'balance')


class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.StringField(source='invoice.invoice_number', read_only=True)
    invoice_id = serializers.UUIDField(source='invoice.uuid', write_only=True)
    product = serializers.StringField(source='product.name', read_only=True)
    product_id = serializers.UUIDField(source='product.uuid', write_only=True, required=False)
    service = serializers.StringField(source='service.name', read_only=True)
    service_id = serializers.UUIDField(source='service.uuid', write_only=True, required=False)
    tax_rate = serializers.StringField(source='tax_rate.name', read_only=True)
    tax_rate_id = serializers.UUIDField(source='tax_rate.uuid', write_only=True, required=False)
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ('uuid', 'total')


class InvoicePaymentSerializer(serializers.ModelSerializer):
    invoice = serializers.StringField(source='invoice.invoice_number', read_only=True)
    invoice_id = serializers.UUIDField(source='invoice.uuid', write_only=True)
    payment_method = serializers.StringField(source='payment_method.name', read_only=True)
    payment_method_id = serializers.UUIDField(source='payment_method.uuid', write_only=True)
    processed_by = serializers.StringField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = InvoicePayment
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at')


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.StringField(source='payment_method.name', read_only=True)
    payment_method_id = serializers.UUIDField(source='payment_method.uuid', write_only=True)
    customer = serializers.StringField(source='customer.full_name', read_only=True)
    customer_id = serializers.UUIDField(source='customer.uuid', write_only=True, required=False)
    supplier = serializers.StringField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True, required=False)
    processed_by = serializers.StringField(source='processed_by.get_full_name', read_only=True)
    processed_by_id = serializers.UUIDField(source='processed_by.uuid', write_only=True, required=False)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'payment_number')


class PaymentMethodSerializer(serializers.ModelSerializer):
    account = serializers.StringField(source='account.code', read_only=True)
    account_id = serializers.UUIDField(source='account.uuid', write_only=True, required=False)
    
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.StringField(source='category.name', read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True)
    payment_method = serializers.StringField(source='payment_method.name', read_only=True)
    payment_method_id = serializers.UUIDField(source='payment_method.uuid', write_only=True, required=False)
    supplier = serializers.StringField(source='supplier.name', read_only=True)
    supplier_id = serializers.UUIDField(source='supplier.uuid', write_only=True, required=False)
    submitted_by = serializers.StringField(source='submitted_by.get_full_name', read_only=True)
    submitted_by_id = serializers.UUIDField(source='submitted_by.uuid', write_only=True, required=False)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    paid_by = serializers.StringField(source='paid_by.get_full_name', read_only=True)
    paid_by_id = serializers.UUIDField(source='paid_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'expense_number', 'total_amount')


class ExpenseCategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = ExpenseCategory
        fields = '__all__'


class TaxRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxRate
        fields = '__all__'


class BudgetCategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = BudgetCategory
        fields = '__all__'


class BudgetSerializer(serializers.ModelSerializer):
    category = BudgetCategorySerializer(read_only=True)
    category_id = serializers.UUIDField(source='category.uuid', write_only=True)
    created_by = serializers.StringField(source='created_by.get_full_name', read_only=True)
    created_by_id = serializers.UUIDField(source='created_by.uuid', write_only=True, required=False)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'used_amount')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
