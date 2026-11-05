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
    list_display = ('name', 'code', 'sequence', 'is_default', 'is_final', 'is_active')
    list_filter = ('is_default', 'is_final', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairPriority)
class RepairPriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level', 'sequence', 'color', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairCategory)
class RepairCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'sequence', 'is_active')
    list_filter = ('parent', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairType)
class RepairTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'estimated_duration', 'base_price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ('repair_number', 'customer', 'device', 'status', 'priority', 'received_date', 'total_cost')
    list_filter = ('status', 'priority', 'category', 'type', 'technician', 'branch', 'organization', 'received_date', 'completed_date')
    search_fields = ('repair_number', 'customer__first_name', 'customer__last_name', 'device__name', 'device__serial_number', 'issue')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('repair_number', 'customer', 'device', 'received_date')
        }),
        (_('Repair Details'), {
            'fields': ('status', 'priority', 'category', 'type', 'issue', 'diagnosis', 'solution')
        }),
        (_('Assignment'), {
            'fields': ('technician', 'assigned_to', 'assigned_at')
        }),
        (_('Financial'), {
            'fields': ('subtotal', 'tax_amount', 'discount', 'total_cost', 'amount_paid', 'balance', 'payment_status')
        }),
        (_('Completion'), {
            'fields': ('completed_date', 'completed_by', 'is_warranty', 'warranty_period')
        }),
        (_('Notes & Metadata'), {
            'fields': ('notes', 'tags', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('customer', 'device', 'technician', 'assigned_to', 'completed_by', 'organization', 'branch')


@admin.register(RepairOrderHistory)
class RepairOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'action', 'performed_by', 'performed_at', 'notes')
    list_filter = ('action', 'performed_at', 'performed_by')
    search_fields = ('repair_order__repair_number', 'notes')
    readonly_fields = ('created_at', 'uuid')
    raw_id_fields = ('repair_order', 'performed_by')


@admin.register(RepairPart)
class RepairPartAdmin(admin.ModelAdmin):
    list_display = ('name', 'part_number', 'category', 'quantity', 'unit_cost', 'total_cost')
    list_filter = ('category',)
    search_fields = ('name', 'part_number', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairService)
class RepairServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'duration', 'price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(RepairChecklist)
class RepairChecklistAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'checklist_template', 'completed_by', 'completed_at', 'is_complete')
    list_filter = ('is_complete', 'completed_at', 'completed_by')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('repair_order', 'checklist_template', 'completed_by')


@admin.register(RepairAttachment)
class RepairAttachmentAdmin(admin.ModelAdmin):
    list_display = ('repair_order', 'name', 'file_type', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    readonly_fields = ('uploaded_at', 'uuid')
    raw_id_fields = ('repair_order', 'uploaded_by')


@admin.register(RepairTemplate)
class RepairTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'estimated_duration', 'base_price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('organization', 'branch')
