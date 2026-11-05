"""
Admin configuration for Suppliers module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SupplierCategory, Supplier, SupplierContact, SupplierDocument


@admin.register(SupplierCategory)
class SupplierCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'sequence', 'is_active')
    list_filter = ('parent', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_number', 'name', 'category', 'email', 'phone', 'status', 'is_active')
    list_filter = ('category', 'status', 'is_active', 'organization', 'branch')
    search_fields = ('supplier_number', 'name', 'email', 'phone', 'tax_id', 'website')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('supplier_number', 'name', 'category', 'website')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'mobile', 'fax')
        }),
        (_('Address'), {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        (_('Business Information'), {
            'fields': ('tax_id', 'business_registration', 'payment_terms', 'credit_limit')
        }),
        (_('Bank Information'), {
            'fields': ('bank_name', 'bank_account', 'bank_branch', 'bank_code')
        }),
        (_('Status & Notes'), {
            'fields': ('status', 'is_active', 'notes', 'tags')
        }),
        (_('Metadata'), {
            'fields': ('uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('organization', 'branch')


@admin.register(SupplierContact)
class SupplierContactAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'first_name', 'last_name', 'email', 'phone', 'position', 'is_primary')
    list_filter = ('supplier', 'position', 'is_primary')
    search_fields = ('supplier__name', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('supplier',)


@admin.register(SupplierDocument)
class SupplierDocumentAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'name', 'document_type', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('supplier__name', 'name', 'description')
    readonly_fields = ('uploaded_at', 'uuid')
    raw_id_fields = ('supplier', 'uploaded_by', 'organization', 'branch')
