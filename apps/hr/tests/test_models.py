"""
Tests for HR models
"""
import pytest
from django.test import TestCase
from apps.hr.models import (
    Department, Position, EmploymentType, Employee, Attendance,
    LeaveType, LeaveRequest, LeaveBalance, Payroll, Overtime,
    Commission, Holiday, Shift, EmployeeDocument
)


class TestDepartment(TestCase):
    """Test Department model"""
    
    def test_department_creation(self):
        """Test creating a department"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        manager = User.objects.create_user(username='manager', email='manager@test.com')
        
        department = Department.objects.create(
            name='Sales',
            code='SALES',
            description='Sales department',
            manager=manager,
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(department.name, 'Sales')
        self.assertEqual(department.code, 'SALES')


class TestPosition(TestCase):
    """Test Position model"""
    
    def test_position_creation(self):
        """Test creating a position"""
        from apps.core.models import Organization, Branch
        
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        department = Department.objects.create(name='Sales', code='SALES', organization=org, branch=branch)
        
        position = Position.objects.create(
            name='Sales Manager',
            code='SM',
            department=department,
            description='Sales manager position',
            minimum_salary=5000.00,
            maximum_salary=10000.00,
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(position.name, 'Sales Manager')
        self.assertEqual(position.minimum_salary, 5000.00)


class TestEmploymentType(TestCase):
    """Test EmploymentType model"""
    
    def test_employment_type_creation(self):
        """Test creating an employment type"""
        employment_type = EmploymentType.objects.create(
            name='Full-time',
            code='FT',
            description='Full-time employment',
            is_active=True
        )
        self.assertEqual(employment_type.name, 'Full-time')


class TestEmployee(TestCase):
    """Test Employee model"""
    
    def test_employee_creation(self):
        """Test creating an employee"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        department = Department.objects.create(name='Sales', code='SALES', organization=org, branch=branch)
        position = Position.objects.create(name='Sales Manager', code='SM', department=department, organization=org, branch=branch)
        employment_type = EmploymentType.objects.create(name='Full-time', code='FT')
        manager = User.objects.create_user(username='manager', email='manager@test.com')
        
        employee = Employee.objects.create(
            employee_number='EMP001',
            first_name='John',
            last_name='Doe',
            position=position,
            department=department,
            employment_type=employment_type,
            manager=manager,
            date_of_birth='1990-01-01',
            gender='male',
            email='john.doe@company.com',
            phone='1234567890',
            mobile='9876543210',
            emergency_contact='Jane Doe (Wife) - 5551234567',
            address='123 Employee St',
            city='Test City',
            state='TC',
            postal_code='12345',
            country='USA',
            national_id='ID123456',
            tax_id='TAX123456',
            social_security_number='SSN123456',
            hire_date='2020-01-01',
            termination_date=None,
            status='active',
            base_salary=7500.00,
            hourly_rate=50.00,
            bank_name='Test Bank',
            bank_account_number='1234567890',
            organization=org,
            branch=branch,
            is_active=True
        )
        self.assertEqual(employee.full_name, 'John Doe')
        self.assertEqual(employee.employee_number, 'EMP001')


class TestAttendance(TestCase):
    """Test Attendance model"""
    
    def test_attendance_creation(self):
        """Test creating an attendance record"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        department = Department.objects.create(name='Sales', code='SALES', organization=org, branch=branch)
        position = Position.objects.create(name='Sales Manager', code='SM', department=department, organization=org, branch=branch)
        employee = Employee.objects.create(
            employee_number='EMP001',
            first_name='John',
            last_name='Doe',
            position=position,
            department=department,
            organization=org,
            branch=branch
        )
        
        attendance = Attendance.objects.create(
            employee=employee,
            date='2023-01-01',
            status='present',
            check_in='2023-01-01T09:00:00',
            check_out='2023-01-01T17:00:00',
            late_minutes=0,
            early_leave_minutes=0,
            organization=org,
            branch=branch
        )
        self.assertEqual(attendance.status, 'present')
        self.assertEqual(attendance.late_minutes, 0)


class TestLeaveType(TestCase):
    """Test LeaveType model"""
    
    def test_leave_type_creation(self):
        """Test creating a leave type"""
        leave_type = LeaveType.objects.create(
            name='Annual Leave',
            code='ANNUAL',
            description='Annual paid leave',
            maximum_days=20,
            is_paid=True,
            requires_approval=True,
            is_active=True
        )
        self.assertEqual(leave_type.name, 'Annual Leave')
        self.assertEqual(leave_type.maximum_days, 20)


class TestLeaveRequest(TestCase):
    """Test LeaveRequest model"""
    
    def test_leave_request_creation(self):
        """Test creating a leave request"""
        from apps.core.models import Organization, Branch
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        org = Organization.objects.create(name='Test Org', code='TO')
        branch = Branch.objects.create(name='Test Branch', code='TB', organization=org)
        department = Department.objects.create(name='Sales', code='SALES', organization=org, branch=branch)
        position = Position.objects.create(name='Sales Manager', code='SM', department=department, organization=org, branch=branch)
        employee = Employee.objects.create(
            employee_number='EMP001',
            first_name='John',
            last_name='Doe',
            position=position,
            department=department,
            organization=org,
            branch=branch
        )
        leave_type = LeaveType.objects.create(name='Annual Leave', code='ANNUAL', maximum_days=20)
        user = User.objects.create_user(username='hr', email='hr@test.com')
        
        leave_request = LeaveRequest.objects.create(
            employee=employee,
            leave_type=leave_type,
            start_date='2023-02-01',
            end_date='2023-02-05',
            status='pending',
            reason='Vacation',
            submitted_by=user,
            organization=org,
            branch=branch
        )
        self.assertEqual(leave_request.status, 'pending')
        self.assertEqual(leave_request.reason, 'Vacation')


class TestHoliday(TestCase):
    """Test Holiday model"""
    
    def test_holiday_creation(self):
        """Test creating a holiday"""
        holiday = Holiday.objects.create(
            name='New Year\'s Day',
            holiday_date='2023-01-01',
            type='public',
            description='New Year celebration',
            is_recurring=True,
            is_active=True
        )
        self.assertEqual(holiday.name, 'New Year\'s Day')
        self.assertEqual(holiday.holiday_date, '2023-01-01')


class TestShift(TestCase):
    """Test Shift model"""
    
    def test_shift_creation(self):
        """Test creating a shift"""
        shift = Shift.objects.create(
            name='Morning Shift',
            code='MORNING',
            start_time='09:00:00',
            end_time='17:00:00',
            description='Morning work shift',
            is_active=True
        )
        self.assertEqual(shift.name, 'Morning Shift')
