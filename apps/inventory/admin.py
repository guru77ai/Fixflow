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
    list_display = ('name', 'code', 'manager', 'is_central', 'is_active')
    list_filter = ('is_active', 'is_central', 'organization', 'branch')
    search_fields = ('name', 'code', 'address', 'phone', 'email')
    readonly_fields = ('uuid',)
    raw_id_fields = ('manager', 'organization', 'branch')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'is_active')
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
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'sku', 'name', 'category', 'brand', 'current_stock', 'purchase_price', 'selling_price', 'is_active')
    list_filter = ('category', 'brand', 'unit', 'is_active', 'stock_type', 'is_serialized', 'is_for_sale', 'organization', 'branch')
    search_fields = ('code', 'sku', 'name', 'barcode', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('code', 'sku', 'barcode', 'name', 'category', 'brand', 'unit')
        }),
        (_('Pricing'), {
            'fields': ('purchase_price', 'selling_price', 'wholesale_price', 'cost_price', 'tax_rate', 'is_taxable')
        }),
        (_('Inventory'), {
            'fields': ('stock_type', 'initial_stock', 'current_stock', 'minimum_stock', 'maximum_stock', 'is_serialized')
        }),
        (_('Product Details'), {
            'fields': ('product_type', 'description', 'specifications', 'is_active', 'is_for_sale', 'is_for_purchase', 'is_for_repair')
        }),
        (_('Warehouse'), {
            'fields': ('warehouse', 'location')
        }),
        (_('Supplier Info'), {
            'fields': ('supplier_code',)
        }),
        (_('Physical Attributes'), {
            'fields': ('weight', 'dimensions', 'color', 'model', 'part_number')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'tags', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('category', 'brand', 'unit', 'warehouse', 'organization', 'branch')


@admin.register(ProductSerialNumber)
class ProductSerialNumberAdmin(admin.ModelAdmin):
    list_display = ('product', 'serial_number', 'batch_number', 'status', 'purchase_date', 'expiry_date')
    list_filter = ('product', 'status', 'purchase_date')
    search_fields = ('serial_number', 'batch_number', 'product__name', 'product__code')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('product', 'organization', 'branch')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'reference_type', 'reference_number', 'created_at')
    list_filter = ('movement_type', 'reference_type', 'product', 'organization', 'branch')
    search_fields = ('product__name', 'product__code', 'reference_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('product', 'source_warehouse', 'destination_warehouse', 'performed_by', 'organization', 'branch')


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ('transfer_number', 'source_warehouse', 'destination_warehouse', 'status', 'transfer_date', 'created_by')
    list_filter = ('status', 'source_warehouse', 'destination_warehouse', 'transfer_date', 'organization', 'branch')
    search_fields = ('transfer_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('source_warehouse', 'destination_warehouse', 'created_by', 'received_by', 'organization', 'branch')


@admin.register(StockTransferItem)
class StockTransferItemAdmin(admin.ModelAdmin):
    list_display = ('transfer', 'product', 'quantity', 'quantity_received', 'unit_cost', 'total_cost')
    list_filter = ('transfer', 'product')
    readonly_fields = ('uuid',)
    raw_id_fields = ('transfer', 'product')


@admin.register(StockAdjustment)
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('adjustment_number', 'date', 'reason', 'performed_by')
    list_filter = ('reason', 'date', 'performed_by', 'organization', 'branch')
    search_fields = ('adjustment_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('performed_by', 'approved_by', 'organization', 'branch')


@admin.register(StockAdjustmentItem)
class StockAdjustmentItemAdmin(admin.ModelAdmin):
    list_display = ('adjustment', 'product', 'old_quantity', 'new_quantity', 'difference', 'unit_cost', 'total_value')
    list_filter = ('adjustment', 'product')
    readonly_fields = ('uuid',)
    raw_id_fields = ('adjustment', 'product')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'estimated_duration', 'price', 'is_active')
    list_filter = ('category', 'service_type', 'is_active', 'is_taxable', 'organization', 'branch')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('category', 'organization', 'branch')


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'is_active')
    list_filter = ('parent', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')
