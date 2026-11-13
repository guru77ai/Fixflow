"""
Admin configuration for Repair module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    RepairStatus, RepairPriority, RepairCategory, RepairType,
    RepairOrder, RepairOrderHistory, RepairPart, RepairService,
    RepairChecklist, RepairAttachment, RepairTemplate
)


@admin.register(RepairStatus)
class RepairStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sequence', 'is_initial', 'is_final')
    list_filter = ('is_initial', 'is_final')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairPriority)
class RepairPriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level', 'estimated_hours', 'color')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairCategory)
class RepairCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'is_active')
    list_filter = ('parent', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairType)
class RepairTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'estimated_duration', 'estimated_cost', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('category',)


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'device_display', 'status', 'priority', 'received_date', 'final_amount')
    list_filter = ('status', 'priority', 'repair_category', 'repair_type', 'assigned_to', 'organization', 'branch', 'received_date', 'completed_date', 'is_approved', 'is_warranty_claim')
    search_fields = ('order_number', 'customer__first_name', 'customer__last_name', 'device__name', 'device_imei', 'device_serial', 'issue_description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('order_number', 'order_type', 'customer', 'device', 'received_date')
        }),
        (_('Device Details'), {
            'fields': ('device_name', 'device_imei', 'device_serial', 'device_brand', 'device_model')
        }),
        (_('Repair Details'), {
            'fields': ('repair_type', 'repair_category', 'status', 'priority', 'issue_description', 'reported_issue', 'diagnosis')
        }),
        (_('Assignment'), {
            'fields': ('assigned_to',)
        }),
        (_('Dates'), {
            'fields': ('promised_date', 'started_date', 'completed_date', 'delivered_date')
        }),
        (_('Financial'), {
            'fields': ('quotation_amount', 'labor_cost', 'parts_cost', 'final_amount', 'discount', 'tax_amount', 'amount_paid', 'balance', 'payment_status', 'payment_method')
        }),
        (_('Warranty'), {
            'fields': ('warranty_type', 'warranty_period', 'warranty_expiry', 'is_warranty_claim')
        }),
        (_('Approval'), {
            'fields': ('is_approved', 'approval_date', 'approved_by')
        }),
        (_('Status Tracking'), {
            'fields': ('is_urgent', 'status_changed_at', 'status_changed_by')
        }),
        (_('Notes'), {
            'fields': ('internal_notes', 'customer_notes', 'notes', 'tags')
        }),
        (_('Metadata'), {
            'fields': ('uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('customer', 'device', 'device_brand', 'device_model', 'repair_type', 'repair_category', 'status', 'priority', 'assigned_to', 'approved_by', 'status_changed_by', 'organization', 'branch')


@admin.register(RepairOrderHistory)
class RepairOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'change_type', 'changed_by', 'created_at', 'comments')
    list_filter = ('change_type', 'created_at', 'changed_by')
    search_fields = ('repair_order__order_number', 'comments')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('repair_order', 'changed_by')


@admin.register(RepairPart)
class RepairPartAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'part_name', 'part_code', 'quantity', 'unit_cost', 'total_cost')
    list_filter = ('repair_order',)
    search_fields = ('repair_order__order_number', 'part_name', 'part_code', 'serial_number')
    readonly_fields = ('uuid',)
    raw_id_fields = ('repair_order', 'part')


@admin.register(RepairService)
class RepairServiceAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'service_name', 'service_code', 'quantity', 'unit_price', 'total_price', 'duration_minutes')
    list_filter = ('repair_order',)
    search_fields = ('repair_order__order_number', 'service_name', 'service_code')
    readonly_fields = ('uuid',)
    raw_id_fields = ('repair_order', 'service', 'technician')


@admin.register(RepairChecklist)
class RepairChecklistAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'item', 'description', 'is_completed', 'completed_at', 'completed_by')
    list_filter = ('is_completed', 'completed_at', 'completed_by')
    search_fields = ('repair_order__order_number', 'item', 'description')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('repair_order', 'completed_by')


@admin.register(RepairAttachment)
class RepairAttachmentAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'title', 'file_type', 'created_at')
    list_filter = ('file_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('repair_order', 'uploaded_by')


@admin.register(RepairTemplate)
class RepairTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'repair_type', 'estimated_duration', 'estimated_cost', 'is_active')
    list_filter = ('repair_type', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('repair_type', 'organization', 'branch')
