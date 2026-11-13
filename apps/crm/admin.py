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
    list_display = ('code', 'full_name', 'email', 'phone', 'status', 'customer_group', 'created_at')
    list_filter = ('status', 'customer_type', 'source', 'customer_group', 'organization', 'branch')
    search_fields = ('code', 'first_name', 'last_name', 'email', 'phone', 'tax_id')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('code', 'first_name', 'last_name', 'email', 'phone', 'mobile')
        }),
        (_('Classification'), {
            'fields': ('customer_type', 'source', 'customer_group')
        }),
        (_('Address'), {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        (_('Additional Info'), {
            'fields': ('tax_id', 'notes', 'profile_image')
        }),
        (_('Metadata'), {
            'fields': ('status', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('organization', 'branch')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'customer', 'brand', 'model', 'serial_number', 'status')
    list_filter = ('status', 'category', 'brand', 'model', 'organization', 'branch')
    search_fields = ('name', 'serial_number', 'imei_1', 'imei_2', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'category')
        }),
        (_('Manufacturer Info'), {
            'fields': ('brand', 'model')
        }),
        (_('Identification'), {
            'fields': ('serial_number', 'imei_1', 'imei_2', 'mac_address')
        }),
        (_('Specifications'), {
            'fields': ('color', 'storage', 'ram', 'os_version')
        }),
        (_('Ownership'), {
            'fields': ('customer', 'purchase_date', 'purchase_price')
        }),
        (_('Warranty'), {
            'fields': ('warranty_expiry',)
        }),
        (_('Metadata'), {
            'fields': ('status', 'is_active', 'notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('customer', 'organization', 'branch')


@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'description')
        }),
        (_('Settings'), {
            'fields': ('is_active', 'color', 'uuid')
        }),
    )


@admin.register(CustomerSource)
class CustomerSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
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
    list_display = ('name', 'code', 'website', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description', 'website')
    readonly_fields = ('uuid',)
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'code', 'description', 'website', 'logo')
        }),
        (_('Settings'), {
            'fields': ('is_active', 'uuid')
        }),
    )


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'brand', 'is_active')
    list_filter = ('brand', 'is_active')
    search_fields = ('name', 'code')
    readonly_fields = ('uuid',)


@admin.register(DeviceCategory)
class DeviceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(CustomerCommunication)
class CustomerCommunicationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'communication_type', 'subject', 'created_at')
    list_filter = ('communication_type', 'direction', 'status', 'organization', 'branch')
    search_fields = ('customer__first_name', 'customer__last_name', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('customer', 'assigned_to')


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'title', 'document_type', 'created_at')
    list_filter = ('document_type', 'is_verified', 'organization', 'branch')
    search_fields = ('customer__first_name', 'customer__last_name', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('customer',)
