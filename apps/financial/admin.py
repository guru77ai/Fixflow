"""
Admin configuration for Financial module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    InvoiceStatus, InvoiceType, Invoice, InvoiceItem, InvoicePayment,
    Payment, Expense, ExpenseCategory, ExpenseAttachment, FinancialReport
)


@admin.register(InvoiceStatus)
class InvoiceStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sequence', 'is_default', 'is_final')
    list_filter = ('is_default', 'is_final')
    search_fields = ('name', 'code')
    readonly_fields = ('uuid',)


@admin.register(InvoiceType)
class InvoiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'prefix', 'description')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'invoice_type', 'customer', 'status', 'total_amount', 'payment_status', 'due_date')
    list_filter = ('invoice_type', 'status', 'payment_status', 'customer', 'supplier', 'due_date', 'paid_date', 'organization', 'branch')
    search_fields = ('invoice_number', 'reference', 'customer__first_name', 'customer__last_name', 'supplier__name')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('invoice_number', 'invoice_type', 'status', 'reference', 'reference_type')
        }),
        (_('Parties'), {
            'fields': ('customer', 'supplier')
        }),
        (_('Financial Details'), {
            'fields': ('subtotal', 'discount', 'tax_amount', 'total_amount', 'amount_paid', 'balance')
        }),
        (_('Payment'), {
            'fields': ('payment_status', 'payment_method', 'payment_reference', 'due_date', 'paid_date')
        }),
        (_('Recurring'), {
            'fields': ('is_recurring', 'recurring_frequency', 'recurring_end_date')
        }),
        (_('Terms & Notes'), {
            'fields': ('terms', 'notes')
        }),
        (_('Metadata'), {
            'fields': ('created_by', 'approved_by', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('invoice_type', 'status', 'customer', 'supplier', 'payment_method', 'created_by', 'approved_by', 'organization', 'branch')


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price', 'tax_amount', 'total_price')
    list_filter = ('invoice',)
    readonly_fields = ('uuid',)
    raw_id_fields = ('invoice', 'product', 'service')


@admin.register(InvoicePayment)
class InvoicePaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'reference')
    list_filter = ('invoice', 'payment_date')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('invoice', 'payment_method', 'processed_by')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_number', 'payment_type', 'amount', 'customer', 'supplier', 'payment_date')
    list_filter = ('payment_type', 'status', 'customer', 'supplier', 'payment_date', 'organization', 'branch')
    search_fields = ('payment_number', 'reference', 'related_to')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('payment_number', 'payment_type', 'amount', 'currency')
        }),
        (_('Parties'), {
            'fields': ('customer', 'supplier')
        }),
        (_('Payment Details'), {
            'fields': ('payment_method', 'reference', 'related_to', 'related_id')
        }),
        (_('Status'), {
            'fields': ('status', 'processed_by', 'approved_by')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('customer', 'supplier', 'payment_method', 'processed_by', 'approved_by', 'organization', 'branch')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_number', 'category', 'title', 'amount', 'expense_date', 'status')
    list_filter = ('category', 'status', 'supplier', 'expense_date', 'paid_date', 'organization', 'branch')
    search_fields = ('expense_number', 'title', 'description', 'supplier__name')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('expense_number', 'category', 'title', 'description')
        }),
        (_('Financial'), {
            'fields': ('amount', 'tax_amount', 'total_amount', 'currency', 'payment_method')
        }),
        (_('Payment'), {
            'fields': ('payment_reference', 'expense_date', 'paid_date')
        }),
        (_('Supplier'), {
            'fields': ('supplier',)
        }),
        (_('Approval'), {
            'fields': ('status', 'submitted_by', 'approved_by', 'paid_by')
        }),
        (_('Metadata'), {
            'fields': ('receipt_attached', 'receipt_file', 'notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('category', 'supplier', 'payment_method', 'submitted_by', 'approved_by', 'paid_by', 'organization', 'branch')


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'is_active')
    list_filter = ('parent', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')


@admin.register(ExpenseAttachment)
class ExpenseAttachmentAdmin(admin.ModelAdmin):
    list_display = ('expense', 'title', 'created_at')
    list_filter = ('expense',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('expense', 'uploaded_by')


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'start_date', 'end_date', 'created_at')
    list_filter = ('report_type', 'start_date', 'end_date', 'organization', 'branch')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('generated_by', 'organization', 'branch')
