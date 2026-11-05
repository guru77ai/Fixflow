"""
Admin configuration for CRM module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Customer, Device, CustomerType, CustomerSource, CustomerGroup,
    DeviceBrand, DeviceModel, DeviceCategory, CustomerCommunication,
    CustomerDocument
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_number', 'full_name', 'email', 'phone', 'status', 'is_vip', 'created_at')
    list_filter = ('status', 'is_vip', 'is_wholesale', 'customer_type', 'source', 'group', 'organization', 'branch')
    search_fields = ('customer_number', 'first_name', 'last_name', 'email', 'phone', 'tax_id')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('customer_number', 'first_name', 'last_name', 'email', 'phone', 'mobile')
        }),
        (_('Classification'), {
            'fields': ('customer_type', 'source', 'group', 'is_vip', 'is_wholesale')
        }),
        (_('Address'), {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        (_('Additional Info'), {
            'fields': ('tax_id', 'notes', 'avatar')
        }),
        (_('Metadata'), {
            'fields': ('status', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('organization', 'branch')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_number', 'name', 'device_type', 'customer', 'brand', 'model', 'serial_number', 'status')
    list_filter = ('status', 'device_type', 'category', 'brand', 'model', 'warranty_status', 'organization', 'branch')
    search_fields = ('device_number', 'name', 'serial_number', 'imei', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('device_number', 'name', 'device_type', 'category')
        }),
        (_('Manufacturer Info'), {
            'fields': ('brand', 'model')
        }),
        (_('Identification'), {
            'fields': ('serial_number', 'imei')
        }),
        (_('Specifications'), {
            'fields': ('color', 'storage', 'os_version', 'description', 'accessories')
        }),
        (_('Ownership'), {
            'fields': ('customer', 'purchase_date')
        }),
        (_('Warranty'), {
            'fields': ('warranty_status', 'warranty_expiry', 'warranty_provider')
        }),
        (_('Metadata'), {
            'fields': ('status', 'notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('customer', 'organization', 'branch')


@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sequence', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'description')
        }),
        (_('Settings'), {
            'fields': ('sequence', 'is_active', 'uuid')
        }),
    )


@admin.register(CustomerSource)
class CustomerSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sequence', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(DeviceBrand)
class DeviceBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'website', 'sequence', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description', 'website')
    readonly_fields = ('uuid',)
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'description', 'website', 'logo')
        }),
        (_('Settings'), {
            'fields': ('sequence', 'is_active', 'uuid')
        }),
    )


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'brand', 'category', 'is_active')
    list_filter = ('brand', 'category', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(DeviceCategory)
class DeviceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'is_active')
    list_filter = ('parent', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(CustomerCommunication)
class CustomerCommunicationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'communication_type', 'subject', 'communication_date', 'created_by')
    list_filter = ('communication_type', 'communication_date', 'created_by')
    search_fields = ('customer__first_name', 'customer__last_name', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('customer', 'created_by')


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'document_type', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'name', 'description')
    readonly_fields = ('uploaded_at', 'uuid')
    raw_id_fields = ('customer', 'uploaded_by')
