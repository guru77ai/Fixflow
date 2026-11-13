"""
Serializers for HR module
"""
from rest_framework import serializers
from .models import (
    Department, Position, EmploymentType, Employee, EmployeeDocument,
    Attendance, LeaveType, LeaveRequest, LeaveBalance, SalaryComponent,
    SalaryStructure, SalaryComponentValue, Payroll, PayrollItem,
    PayrollComponent, Commission, Overtime, HRReport
)


class DepartmentSerializer(serializers.ModelSerializer):
    manager = serializers.CharField(source='manager.get_full_name', read_only=True)
    manager_id = serializers.UUIDField(source='manager.uuid', write_only=True, required=False)
    parent = serializers.CharField(source='parent.name', read_only=True)
    parent_id = serializers.UUIDField(source='parent.uuid', write_only=True, required=False)
    
    class Meta:
        model = Department
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.UUIDField(source='department.uuid', write_only=True, required=False)
    
    class Meta:
        model = Position
        fields = '__all__'


class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.get_full_name', read_only=True)
    user_id = serializers.UUIDField(source='user.uuid', write_only=True, required=False)
    department = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.UUIDField(source='department.uuid', write_only=True, required=False)
    position = serializers.CharField(source='position.name', read_only=True)
    position_id = serializers.UUIDField(source='position.uuid', write_only=True, required=False)
    employment_type = serializers.CharField(source='employment_type.name', read_only=True)
    employment_type_id = serializers.UUIDField(source='employment_type.uuid', write_only=True, required=False)
    manager = serializers.CharField(source='manager.get_full_name', read_only=True)
    manager_id = serializers.UUIDField(source='manager.uuid', write_only=True, required=False)
    branch = serializers.CharField(source='branch.name', read_only=True)
    branch_id = serializers.UUIDField(source='branch.uuid', write_only=True, required=False)
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'employee_number')


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    uploaded_by = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeeDocument
        fields = '__all__'
        read_only_fields = ('uuid', 'uploaded_at')


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    leave_type = serializers.CharField(source='leave_type.name', read_only=True)
    leave_type_id = serializers.UUIDField(source='leave_type.uuid', write_only=True)
    approved_by = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'request_number')


class LeaveBalanceSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    leave_type = serializers.CharField(source='leave_type.name', read_only=True)
    leave_type_id = serializers.UUIDField(source='leave_type.uuid', write_only=True)
    
    class Meta:
        model = LeaveBalance
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at')


class SalaryComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = '__all__'


class SalaryStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryStructure
        fields = '__all__'


class SalaryComponentValueSerializer(serializers.ModelSerializer):
    salary_structure = serializers.CharField(source='salary_structure.name', read_only=True)
    salary_structure_id = serializers.UUIDField(source='salary_structure.uuid', write_only=True)
    salary_component = serializers.CharField(source='salary_component.name', read_only=True)
    salary_component_id = serializers.UUIDField(source='salary_component.uuid', write_only=True)
    
    class Meta:
        model = SalaryComponentValue
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    
    class Meta:
        model = Payroll
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'payroll_number')


class PayrollItemSerializer(serializers.ModelSerializer):
    payroll = serializers.CharField(source='payroll.payroll_number', read_only=True)
    payroll_id = serializers.UUIDField(source='payroll.uuid', write_only=True)
    salary_component = serializers.CharField(source='salary_component.name', read_only=True)
    salary_component_id = serializers.UUIDField(source='salary_component.uuid', write_only=True)
    
    class Meta:
        model = PayrollItem
        fields = '__all__'


class PayrollComponentSerializer(serializers.ModelSerializer):
    payroll = serializers.CharField(source='payroll.payroll_number', read_only=True)
    payroll_id = serializers.UUIDField(source='payroll.uuid', write_only=True)
    salary_component = serializers.CharField(source='salary_component.name', read_only=True)
    salary_component_id = serializers.UUIDField(source='salary_component.uuid', write_only=True)
    
    class Meta:
        model = PayrollComponent
        fields = '__all__'


class CommissionSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    
    class Meta:
        model = Commission
        fields = '__all__'


class OvertimeSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.UUIDField(source='employee.uuid', write_only=True)
    approved_by = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    approved_by_id = serializers.UUIDField(source='approved_by.uuid', write_only=True, required=False)
    
    class Meta:
        model = Overtime
        fields = '__all__'


class HRReportSerializer(serializers.ModelSerializer):
    generated_by = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    
    class Meta:
        model = HRReport
        fields = '__all__'
        read_only_fields = ('uuid', 'created_at', 'updated_at', 'generated_at')
