"""
Admin configuration for HR module
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Department, Position, EmploymentType, Employee, Attendance,
    LeaveType, LeaveRequest, LeaveBalance, Payroll, Overtime,
    Commission, Holiday, Shift, EmployeeDocument
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'manager', 'parent', 'is_active')
    list_filter = ('parent', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description', 'manager__first_name', 'manager__last_name')
    readonly_fields = ('uuid',)
    raw_id_fields = ('manager', 'organization', 'branch')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'minimum_salary', 'maximum_salary', 'is_active')
    list_filter = ('department', 'is_active', 'organization', 'branch')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)
    raw_id_fields = ('department', 'organization', 'branch')


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_number', 'full_name', 'position', 'department', 'status', 'hire_date')
    list_filter = ('position', 'department', 'employment_type', 'status', 'gender', 'hire_date', 'termination_date', 'organization', 'branch')
    search_fields = ('employee_number', 'first_name', 'last_name', 'email', 'phone', 'national_id')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('employee_number', 'first_name', 'last_name', 'date_of_birth', 'gender', 'avatar')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'mobile', 'emergency_contact')
        }),
        (_('Address'), {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        (_('Employment'), {
            'fields': ('position', 'department', 'employment_type', 'manager', 'hire_date', 'termination_date', 'status')
        }),
        (_('Compensation'), {
            'fields': ('base_salary', 'hourly_rate', 'currency')
        }),
        (_('Identification'), {
            'fields': ('national_id', 'tax_id', 'social_security_number')
        }),
        (_('Bank Information'), {
            'fields': ('bank_name', 'bank_account_number')
        }),
        (_('Status & Notes'), {
            'fields': ('is_active', 'notes', 'tags')
        }),
        (_('Metadata'), {
            'fields': ('uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('position', 'department', 'employment_type', 'manager', 'organization', 'branch')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'check_in', 'check_out', 'late_minutes', 'early_leave_minutes')
    list_filter = ('employee', 'date', 'status', 'organization', 'branch')
    search_fields = ('employee__first_name', 'employee__last_name', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('employee', 'approved_by', 'organization', 'branch')


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'maximum_days', 'is_paid', 'requires_approval', 'is_active')
    list_filter = ('is_paid', 'requires_approval', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'days_requested', 'status')
    list_filter = ('employee', 'leave_type', 'status', 'start_date', 'end_date', 'organization', 'branch')
    search_fields = ('employee__first_name', 'employee__last_name', 'reason')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('employee', 'leave_type', 'start_date', 'end_date', 'days_requested')
        }),
        (_('Approval'), {
            'fields': ('status', 'reason', 'submitted_by', 'approved_by', 'rejected_by', 'rejection_reason')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('employee', 'leave_type', 'submitted_by', 'approved_by', 'rejected_by', 'organization', 'branch')


@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'year', 'allocated_days', 'used_days', 'remaining_days')
    list_filter = ('employee', 'leave_type', 'year')
    readonly_fields = ('uuid',)
    raw_id_fields = ('employee', 'leave_type')


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('payroll_number', 'period_start', 'period_end', 'total_gross', 'total_deductions', 'total_net', 'status')
    list_filter = ('status', 'period_start', 'period_end', 'payment_date', 'organization', 'branch')
    search_fields = ('payroll_number', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('payroll_number', 'period_start', 'period_end')
        }),
        (_('Financial Summary'), {
            'fields': ('total_gross', 'total_deductions', 'total_net', 'currency')
        }),
        (_('Payment'), {
            'fields': ('payment_date', 'payment_method')
        }),
        (_('Status & Approval'), {
            'fields': ('status', 'created_by', 'approved_by', 'paid_by')
        }),
        (_('Metadata'), {
            'fields': ('notes', 'uuid', 'created_at', 'updated_at')
        }),
    )
    raw_id_fields = ('payment_method', 'created_by', 'approved_by', 'paid_by', 'organization', 'branch')


@admin.register(Overtime)
class OvertimeAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'hours', 'rate', 'is_approved', 'is_paid')
    list_filter = ('employee', 'date', 'is_approved', 'is_paid', 'organization', 'branch')
    search_fields = ('employee__first_name', 'employee__last_name', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('employee', 'approved_by', 'organization', 'branch')


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'period_start', 'period_end', 'amount', 'percentage', 'is_paid')
    list_filter = ('employee', 'period_start', 'period_end', 'is_paid', 'organization', 'branch')
    search_fields = ('employee__first_name', 'employee__last_name', 'reference', 'notes')
    readonly_fields = ('created_at', 'updated_at', 'uuid')
    raw_id_fields = ('employee', 'organization', 'branch')


@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('name', 'holiday_date', 'type', 'is_recurring', 'is_active')
    list_filter = ('type', 'is_recurring', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('uuid',)


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('uuid',)


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'name', 'document_type', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('employee__first_name', 'employee__last_name', 'name', 'description')
    readonly_fields = ('uploaded_at', 'uuid')
    raw_id_fields = ('employee', 'uploaded_by', 'organization', 'branch')
