"""
Serializers for HR module
"""
from rest_framework import serializers
from .models import (
    Department, Position, EmploymentType, Employee, Attendance,
    LeaveType, LeaveRequest, LeaveBalance, Payroll, Overtime,
    Commission, Holiday, Shift, EmployeeDocument
)


class DepartmentSerializer(serializers.ModelSerializer):
    manager = serializers.StringField(source='manager.get_full_name', read_only=True)
    manager_id = serializers.UUIDField(source='manager.uuid', write_only=True, required=False)
    parent = serializers.StringField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.UUIDField(source='department.uuid', write_only=True, required=False)
    
    class Meta:
        model = Position
        fields = '__all__'


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)
    position_id = serializers.UUIDField(source='position.uuid', write_only=True, required=False)
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.UUIDField(source='department.uuid', write_only=True, required=False)
    employment_type = EmploymentTypeSerializer(read_only=True)
    employment_type_id = serializers.UUIDField(source='employment_type.uuid', write_only=True, required=False)
    manager = serializers.StringField(source='manager.get_full_name', read_only=True)
    manager_id = serializers.UUIDField(source='manager.uuid', write_only=True, required=False)
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'employee_number')


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.StringField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.StringField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    leave_type = LeaveTypeSerializer(read_only=True)
    leave_type_id = serializers.UUIDField(source='leave_type.uuid', write_only=True)
    submitted_by = serializers.StringField(source='submitted_by.get_full_name', read_only=True)
    submitted_by_id = serializers.UUIDField(source='submitted_by.uuid', write_only=True, required=False)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    rejected_by = serializers.StringField(source='rejected_by.get_full_name', read_only=True)
    rejected_by_id = serializers.UUIDField(source='rejected_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'days_requested')


class LeaveBalanceSerializer(serializers.ModelSerializer):
    employee = serializers.StringField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    leave_type = LeaveTypeSerializer(read_only=True)
    leave_type_id = serializers.UUIDField(source='leave_type.uuid', write_only=True)
    
    class Meta:
        model = LeaveBalance
        fields = '__all__'
        read_only_fields = ('uuid',)


class PayrollSerializer(serializers.ModelSerializer):
    created_by = serializers.StringField(source='created_by.get_full_name', read_only=True)
    created_by_id = serializers.UUIDField(source='created_by.uuid', write_only=True, required=False)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    paid_by = serializers.StringField(source='paid_by.get_full_name', read_only=True)
    paid_by_id = serializers.UUIDField(source='paid_by.uuid', write_only=True, required=False)
    payment_method = serializers.StringField(source='payment_method.name', read_only=True)
    payment_method_id = serializers.UUIDField(source='payment_method.uuid', write_only=True, required=False)
    
    class Meta:
        model = Payroll
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'payroll_number', 'total_gross', 'total_deductions', 'total_net')


class OvertimeSerializer(serializers.ModelSerializer):
    employee = serializers.StringField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    approved_by = serializers.StringField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Overtime
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'net_amount')


class CommissionSerializer(serializers.ModelSerializer):
    employee = serializers.StringField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    
    class Meta:
        model = Commission
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'amount')


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = '__all__'


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    employee = serializers.StringField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    uploaded_by = serializers.StringField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeeDocument
        fields = '__all__'
        read_only_fields = ('uuid', 'uploaded_at')
