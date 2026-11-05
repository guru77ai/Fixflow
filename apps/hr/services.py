"""Services for HR module"""
from django.db import transaction
from decimal import Decimal
from .models import Employee, Attendance, LeaveRequest, LeaveBalance, Payroll, Overtime, Commission


class EmployeeService:
    @staticmethod
    @transaction.atomic
    def create_employee(data, organization, branch, created_by=None):
        employee = Employee.objects.create(
            organization=organization,
            branch=branch,
            employee_number=EmployeeService.generate_employee_number(organization, branch),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            position_id=data.get('position_id'),
            department_id=data.get('department_id'),
            employment_type_id=data.get('employment_type_id'),
            manager_id=data.get('manager_id'),
            date_of_birth=data.get('date_of_birth'),
            gender=data.get('gender'),
            email=data.get('email'),
            phone=data.get('phone'),
            mobile=data.get('mobile'),
            emergency_contact=data.get('emergency_contact'),
            address=data.get('address'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country', 'Algeria'),
            national_id=data.get('national_id'),
            tax_id=data.get('tax_id'),
            social_security_number=data.get('social_security_number'),
            hire_date=data.get('hire_date'),
            termination_date=data.get('termination_date'),
            status=data.get('status', 'active'),
            base_salary=Decimal(data.get('base_salary', 0) or 0),
            hourly_rate=Decimal(data.get('hourly_rate', 0) or 0),
            bank_name=data.get('bank_name'),
            bank_account_number=data.get('bank_account_number'),
            is_active=data.get('is_active', True),
            notes=data.get('notes'),
        )
        return employee
    
    @staticmethod
    def generate_employee_number(organization, branch):
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        last_emp = Employee.objects.filter(employee_number__startswith=f"{org_code}-{branch_code}").order_by('-employee_number').first()
        seq = 1
        if last_emp:
            try:
                seq = int(last_emp.employee_number.split('-')[-1]) + 1
            except:
                seq = 1
        return f"{org_code}-{branch_code}-{seq:04d}"


class AttendanceService:
    @staticmethod
    @transaction.atomic
    def record_attendance(data, organization, branch, created_by=None):
        attendance = Attendance.objects.create(
            organization=organization,
            branch=branch,
            employee_id=data.get('employee_id'),
            date=data.get('date'),
            status=data.get('status', 'present'),
            check_in=data.get('check_in'),
            check_out=data.get('check_out'),
            late_minutes=data.get('late_minutes', 0),
            early_leave_minutes=data.get('early_leave_minutes', 0),
            notes=data.get('notes'),
        )
        return attendance


class LeaveRequestService:
    @staticmethod
    @transaction.atomic
    def create_leave_request(data, organization, branch, created_by=None):
        leave_request = LeaveRequest.objects.create(
            organization=organization,
            branch=branch,
            employee_id=data.get('employee_id'),
            leave_type_id=data.get('leave_type_id'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            status=data.get('status', 'draft'),
            reason=data.get('reason'),
            submitted_by=created_by,
            approved_by_id=data.get('approved_by_id'),
            rejected_by_id=data.get('rejected_by_id'),
            rejection_reason=data.get('rejection_reason'),
        )
        
        # Update leave balance
        if leave_request.status == 'approved':
            LeaveRequestService.update_leave_balance(leave_request)
        
        return leave_request
    
    @staticmethod
    def update_leave_balance(leave_request):
        """Update employee leave balance"""
        year = leave_request.start_date.year
        leave_type = leave_request.leave_type
        employee = leave_request.employee
        
        # Get or create leave balance
        balance, created = LeaveBalance.objects.get_or_create(
            employee=employee,
            leave_type=leave_type,
            year=year,
            defaults={'allocated_days': leave_type.maximum_days, 'used_days': 0, 'remaining_days': leave_type.maximum_days}
        )
        
        # Update used days
        days = leave_request.days_requested
        balance.used_days += days
        balance.remaining_days = balance.allocated_days - balance.used_days
        balance.save()


class PayrollService:
    @staticmethod
    @transaction.atomic
    def create_payroll(data, organization, branch, created_by=None):
        payroll = Payroll.objects.create(
            organization=organization,
            branch=branch,
            payroll_number=PayrollService.generate_payroll_number(organization, branch),
            period_start=data.get('period_start'),
            period_end=data.get('period_end'),
            status=data.get('status', 'draft'),
            total_gross=Decimal(data.get('total_gross', 0) or 0),
            total_deductions=Decimal(data.get('total_deductions', 0) or 0),
            total_net=Decimal(data.get('total_net', 0) or 0),
            payment_date=data.get('payment_date'),
            created_by=created_by,
            approved_by_id=data.get('approved_by_id'),
            paid_by_id=data.get('paid_by_id'),
            notes=data.get('notes'),
        )
        return payroll
    
    @staticmethod
    def generate_payroll_number(organization, branch):
        from django.utils import timezone
        org_code = organization.code if organization else 'ORG'
        branch_code = branch.code if branch else 'BR'
        date_str = timezone.now().strftime('%Y%m')
        last_pay = Payroll.objects.filter(payroll_number__startswith=f"{org_code}-{branch_code}-{date_str}").order_by('-payroll_number').first()
        seq = 1
        if last_pay:
            try:
                seq = int(last_pay.payroll_number.split('-')[-1]) + 1
            except:
                seq = 1
        return f"{org_code}-{branch_code}-{date_str}-{seq:02d}"


class OvertimeService:
    @staticmethod
    @transaction.atomic
    def record_overtime(data, organization, branch, created_by=None):
        overtime = Overtime.objects.create(
            organization=organization,
            branch=branch,
            employee_id=data.get('employee_id'),
            date=data.get('date'),
            hours=Decimal(data.get('hours', 0) or 0),
            rate=Decimal(data.get('rate', 0) or 0),
            is_approved=data.get('is_approved', False),
            approved_by_id=data.get('approved_by_id'),
            is_paid=data.get('is_paid', False),
            paid_date=data.get('paid_date'),
            notes=data.get('notes'),
        )
        return overtime


class CommissionService:
    @staticmethod
    @transaction.atomic
    def record_commission(data, organization, branch, created_by=None):
        commission = Commission.objects.create(
            organization=organization,
            branch=branch,
            employee_id=data.get('employee_id'),
            period_start=data.get('period_start'),
            period_end=data.get('period_end'),
            amount=Decimal(data.get('amount', 0) or 0),
            percentage=Decimal(data.get('percentage', 0) or 0),
            base_amount=Decimal(data.get('base_amount', 0) or 0),
            reference=data.get('reference'),
            reference_type=data.get('reference_type'),
            is_paid=data.get('is_paid', False),
            paid_date=data.get('paid_date'),
            notes=data.get('notes'),
        )
        return commission
