"""
Admin configuration for Inventory module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Warehouse, ProductCategory, ProductBrand, UnitOfMeasure,
    Product, ProductSerialNumber, StockMovement, StockTransfer,
    StockTransferItem, StockAdjustment, StockAdjustmentItem,
    Service, ServiceCategory
)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'manager', 'location', 'is_active')
    list_filter = ('is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'location', 'manager__first_name', 'manager__last_name')
    readonly_fields = ('uuid',)
    raw_id_fields = ('manager', 'organization', 'branch')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'sequence', 'is_active')
    list_filter = ('parent', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'website', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description', 'website')
    readonly_fields = ('uuid',)


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'symbol', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'symbol')
    readonly_fields = ('uuid',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'brand', 'current_stock', 'unit_cost', 'selling_price', 'is_active')
    list_filter = ('category', 'brand', 'uom', 'is_active', 'is_serialized', 'is_service', 'organization', 'branch')
    search_fields = ('sku', 'name', 'barcode', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('sku', 'name', 'barcode', 'category', 'brand', 'uom')
        }),
        (_('Pricing'), {
            'fields': ('unit_cost', 'selling_price', 'tax_rate', 'discount_rate')
        }),
        (_('Inventory'), {
            'fields': ('initial_stock', 'current_stock', 'minimum_stock', 'maximum_stock', 'is_serialized')
        }),
        (_('Product Details'), {
            'fields': ('description', 'specifications', 'is_active', 'is_service')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'tags', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('organization', 'branch')


@admin.register(ProductSerialNumber)
class ProductSerialNumberAdmin(admin.ModelAdmin):
    list_display = ('product', 'serial_number', 'status', 'purchase_date', 'warranty_expiry')
    list_filter = ('product', 'status', 'purchase_date', 'warranty_expiry')
    search_fields = ('serial_number', 'product__name', 'product__sku')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('product', 'purchase_order', 'sales_order', 'organization', 'branch')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'reference', 'date', 'created_by')
    list_filter = ('movement_type', 'date', 'created_by', 'organization', 'branch')
    search_fields = ('product__name', 'product__sku', 'reference', 'notes')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('product', 'created_by', 'organization', 'branch')


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_number', 'from_warehouse', 'to_warehouse', 'status', 'transfer_date', 'created_by')
    list_filter = ('status', 'from_warehouse', 'to_warehouse', 'transfer_date', 'created_by', 'organization', 'branch')
    search_fields = ('transfer_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('from_warehouse', 'to_warehouse', 'created_by', 'approved_by', 'received_by', 'organization', 'branch')


@admin.register(StockTransferItem)
class StockTransferItemAdmin(admin.ModelAdmin):
    list_display = ('transfer', 'product', 'quantity', 'batch_number')
    list_filter = ('transfer', 'product')
    readonly_fields = ('uuid',)
    raw_id_fields = ('transfer', 'product')


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('adjustment_number', 'warehouse', 'adjustment_type', 'status', 'adjustment_date', 'created_by')
    list_filter = ('adjustment_type', 'status', 'warehouse', 'adjustment_date', 'created_by', 'organization', 'branch')
    search_fields = ('adjustment_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('warehouse', 'created_by', 'approved_by', 'organization', 'branch')


@admin.register(StockAdjustmentItem)
class StockAdjustmentItemAdmin(admin.ModelAdmin):
    list_display = ('adjustment', 'product', 'quantity', 'reason')
    list_filter = ('adjustment', 'product')
    readonly_fields = ('uuid',)
    raw_id_fields = ('adjustment', 'product')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_number', 'name', 'category', 'duration', 'price', 'is_active')
    list_filter = ('category', 'is_active', 'organization', 'branch')
    search_fields = ('service_number', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('category', 'organization', 'branch')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'sequence', 'is_active')
    list_filter = ('parent', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')
