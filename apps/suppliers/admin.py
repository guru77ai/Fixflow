"""
Admin configuration for Suppliers module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SupplierCategory, Supplier, SupplierContact, SupplierDocument


@admin.register(SupplierCategory)
class SupplierCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'email', 'phone', 'status')
    list_filter = ('category', 'status', 'is_verified', 'is_preferred', 'organization', 'branch')
    search_fields = ('code', 'name', 'company_name', 'email', 'phone', 'tax_id', 'website')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('code', 'name', 'company_name', 'category', 'website')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'mobile')
        }),
        (_('Address'), {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        (_('Business Information'), {
            'fields': ('tax_id', 'payment_terms', 'credit_limit', 'credit_balance')
        }),
        (_('Ratings'), {
            'fields': ('quality_rating', 'delivery_rating')
        }),
        (_('Status & Notes'), {
            'fields': ('status', 'is_verified', 'is_preferred', 'is_active', 'notes')
        }),
        (_('Account Manager'), {
            'fields': ('account_manager',)
        }),
        (_('Metadata'), {
            'fields': ('uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('category', 'account_manager', 'organization', 'branch')


@admin.register(SupplierContact)
class SupplierContactAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'first_name', 'last_name', 'email', 'phone', 'position', 'is_primary')
    list_filter = ('supplier', 'position', 'is_primary')
    search_fields = ('supplier__name', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('supplier',)


@admin.register(SupplierDocument)
class SupplierDocumentAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'title', 'document_type', 'created_at')
    list_filter = ('document_type', 'is_verified', 'organization', 'branch')
    search_fields = ('supplier__name', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('supplier', 'organization', 'branch')
