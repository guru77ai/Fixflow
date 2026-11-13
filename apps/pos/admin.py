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
    list_display = ('name', 'code', 'is_cash', 'is_card', 'is_mobile', 'is_online', 'is_active')
    list_filter = ('is_cash', 'is_card', 'is_mobile', 'is_online', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'current_amount', 'is_open', 'is_active')
    list_filter = ('is_active', 'is_open', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('organization', 'branch', 'opened_by', 'closed_by')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_number', 'customer', 'total_amount', 'payment_status', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'sale_type', 'customer', 'cash_register', 'is_credit', 'organization', 'branch')
    search_fields = ('sale_number', 'customer__first_name', 'customer__last_name', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('sale_number', 'customer', 'cash_register', 'sale_type')
        }),
        (_('Financial'), {
            'fields': ('subtotal', 'discount', 'tax_amount', 'total_amount', 'amount_paid', 'balance', 'payment_status')
        }),
        (_('Payment'), {
            'fields': ('payment_method', 'payment_reference', 'is_credit', 'credit_days', 'due_date')
        }),
        (_('Invoice'), {
            'fields': ('is_invoice', 'invoice_number')
        }),
        (_('Status'), {
            'fields': ('status',)
        }),
        (_('Metadata'), {
            'fields': ('notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('customer', 'cash_register', 'payment_method', 'sold_by', 'organization', 'branch')


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'product_name', 'quantity', 'unit_price', 'total_price')
    list_filter = ('sale', 'product')
    readonly_fields = ('uuid',)
    raw_id_fields = ('sale', 'product', 'service')


@admin.register(SalePayment)
class SalePaymentAdmin(admin.ModelAdmin):
    list_display = ('sale', 'payment_method', 'amount', 'reference', 'payment_date')
    list_filter = ('sale', 'payment_method', 'payment_date', 'status')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('sale', 'payment_method', 'processed_by')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('sale', 'receipt_number', 'receipt_type', 'is_printed', 'is_emailed')
    list_filter = ('receipt_type', 'is_printed', 'is_emailed')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('sale', 'printed_by')


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('refund_number', 'sale', 'amount', 'status', 'created_at')
    list_filter = ('status', 'reason', 'sale', 'organization', 'branch')
    search_fields = ('refund_number', 'sale__sale_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('sale', 'payment_method', 'requested_by', 'approved_by', 'processed_by', 'organization', 'branch')


@admin.register(RefundItem)
class RefundItemAdmin(admin.ModelAdmin):
    list_display = ('refund', 'sale_item', 'product_name', 'quantity', 'unit_price', 'total_price')
    list_filter = ('refund', 'product_name')
    readonly_fields = ('uuid',)
    raw_id_fields = ('refund', 'sale_item')


@admin.register(POSSession)
class POSSessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'cash_register', 'user', 'started_at', 'ended_at', 'is_active')
    list_filter = ('cash_register', 'user', 'is_active', 'started_at', 'ended_at', 'organization', 'branch')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('cash_register', 'user', 'organization', 'branch')


@admin.register(POSSettings)
class POSSettingsAdmin(admin.ModelAdmin):
    list_display = ('default_payment_method', 'default_cash_register', 'show_customer_display', 'auto_print_receipt', 'auto_email_receipt', 'default_tax_rate')
    list_filter = ('auto_print_receipt', 'auto_email_receipt', 'show_customer_display', 'tax_included', 'allow_credit_sales')
    readonly_fields = ('uuid',)
    raw_id_fields = ('default_payment_method', 'default_cash_register', 'organization', 'branch')
