"""
Admin configuration for POS module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    PaymentMethod, CashRegister, Sale, SaleItem, SalePayment,
    Receipt, Refund, RefundItem, POSSession, POSSettings
)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'is_active')
    list_filter = ('type', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'current_balance', 'status', 'is_active')
    list_filter = ('status', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('organization', 'branch')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_number', 'customer', 'total_amount', 'payment_status', 'status', 'sale_date')
    list_filter = ('status', 'payment_status', 'sale_type', 'customer', 'cash_register', 'sale_date', 'organization', 'branch')
    search_fields = ('sale_number', 'customer__first_name', 'customer__last_name', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('sale_number', 'customer', 'cash_register', 'sale_date', 'sale_type')
        }),
        (_('Financial'), {
            'fields': ('subtotal', 'tax_amount', 'discount', 'total_amount', 'amount_paid', 'balance', 'payment_status')
        }),
        (_('Status'), {
            'fields': ('status', 'is_returned')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'tags', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('customer', 'cash_register', 'technician', 'organization', 'branch')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'unit_price', 'total_price')
    list_filter = ('sale', 'product')
    readonly_fields = ('uuid',)
    raw_id_fields = ('sale', 'product', 'service')


@admin.register(SalePayment)
class SalePaymentAdmin(admin.ModelAdmin):
    list_display = ('sale', 'payment_method', 'amount', 'transaction_reference', 'payment_date')
    list_filter = ('sale', 'payment_method', 'payment_date')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('sale', 'payment_method', 'processed_by')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('sale', 'receipt_number', 'receipt_type', 'print_count', 'email_sent')
    list_filter = ('receipt_type', 'email_sent', 'printed_at')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('sale', 'customer', 'created_by')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('refund_number', 'sale', 'total_amount', 'status', 'refund_date')
    list_filter = ('status', 'refund_type', 'sale', 'refund_date', 'organization', 'branch')
    search_fields = ('refund_number', 'sale__sale_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('sale', 'customer', 'processed_by', 'approved_by', 'organization', 'branch')


@admin.register(RefundItem)
class RefundItemAdmin(admin.ModelAdmin):
    list_display = ('refund', 'sale_item', 'product', 'quantity', 'unit_price', 'total_price')
    list_filter = ('refund', 'product')
    readonly_fields = ('uuid',)
    raw_id_fields = ('refund', 'sale_item', 'product')


@admin.register(POSSession)
class POSSessionAdmin(admin.ModelAdmin):
    list_display = ('session_number', 'cash_register', 'user', 'start_time', 'end_time', 'status')
    list_filter = ('cash_register', 'user', 'status', 'start_time', 'end_time', 'organization', 'branch')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('cash_register', 'user', 'organization', 'branch')


@admin.register(POSSettings)
class POSSettingsAdmin(admin.ModelAdmin):
    list_display = ('default_receipt_type', 'auto_print_receipt', 'show_customer_display', 'enable_tips', 'default_tax_rate')
    list_filter = ('auto_print_receipt', 'show_customer_display', 'enable_tips')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')
