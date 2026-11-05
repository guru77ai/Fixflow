"""
HR Models for FixSoftRepair Pro
Human Resources module
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from apps.core.models import TimeStampedModel, UUIDModel, OrganizationAndBranchScopedModel, NoteModel, CurrencyField


class Department(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Department model"""
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name=_('Parent Department'))
    
    manager = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_departments', verbose_name=_('Manager'))
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name


class Position(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Job position"""
    name = models.CharField(_('Name'), max_length=100)
    code = models.CharField(_('Code'), max_length=20, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='positions', verbose_name=_('Department'))
    
    minimum_salary = CurrencyField(_('Minimum Salary'), default=0.00)
    maximum_salary = CurrencyField(_('Maximum Salary'), default=0.00)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        ordering = ['name']
        unique_together = [['organization', 'code']]
    
    def __str__(self):
        return self.name


class EmploymentType(UUIDModel, TimeStampedModel):
    """Employment type"""
    name = models.CharField(_('Name'), max_length=100, unique=True)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Employment Type')
        verbose_name_plural = _('Employment Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Employee(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel, NoteModel):
    """Employee model"""
    EMPLOYEE_STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('on_leave', _('On Leave')),
        ('terminated', _('Terminated')),
        ('retired', _('Retired')),
    ]
    
    GENDER_CHOICES = [
        ('male', _('Male')),
        ('female', _('Female')),
        ('other', _('Other')),
    ]
    
    employee_number = models.CharField(_('Employee Number'), max_length=20, unique=True)
    
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    full_name = models.CharField(_('Full Name'), max_length=200, blank=True, null=True)
    
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name=_('Position'))
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name=_('Department'))
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees', verbose_name=_('Employment Type'))
    
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates', verbose_name=_('Manager'))
    
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    
    email = models.EmailField(_('Email'), blank=True, null=True)
    phone = PhoneNumberField(_('Phone'), blank=True, null=True)
    mobile = PhoneNumberField(_('Mobile'), blank=True, null=True)
    emergency_contact = PhoneNumberField(_('Emergency Contact'), blank=True, null=True)
    
    address = models.TextField(_('Address'), blank=True, null=True)
    city = models.CharField(_('City'), max_length=100, blank=True, null=True)
    state = models.CharField(_('State'), max_length=100, blank=True, null=True)
    postal_code = models.CharField(_('Postal Code'), max_length=20, blank=True, null=True)
    country = models.CharField(_('Country'), max_length=100, default='Algeria')
    
    national_id = models.CharField(_('National ID'), max_length=50, blank=True, null=True)
    tax_id = models.CharField(_('Tax ID'), max_length=50, blank=True, null=True)
    social_security_number = models.CharField(_('Social Security Number'), max_length=50, blank=True, null=True)
    
    hire_date = models.DateField(_('Hire Date'))
    termination_date = models.DateField(_('Termination Date'), blank=True, null=True)
    status = models.CharField(_('Status'), max_length=20, choices=EMPLOYEE_STATUS_CHOICES, default='active')
    
    base_salary = CurrencyField(_('Base Salary'), default=0.00)
    hourly_rate = CurrencyField(_('Hourly Rate'), default=0.00)
    
    bank_name = models.CharField(_('Bank Name'), max_length=200, blank=True, null=True)
    bank_account_number = models.CharField(_('Bank Account Number'), max_length=50, blank=True, null=True)
    
    profile_image = models.ImageField(_('Profile Image'), upload_to='employees/images/', blank=True, null=True)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['employee_number']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['position']),
            models.Index(fields=['department']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_number})"
    
    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)


class EmployeeDocument(UUIDModel, TimeStampedModel):
    """Employee documents"""
    DOCUMENT_TYPE_CHOICES = [
        ('id_card', _('ID Card')),
        ('passport', _('Passport')),
        ('resume', _('Resume')),
        ('contract', _('Contract')),
        ('certificate', _('Certificate')),
        ('diploma', _('Diploma')),
        ('other', _('Other')),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='documents', verbose_name=_('Employee'))
    document_type = models.CharField(_('Document Type'), max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(_('Title'), max_length=200)
    file = models.FileField(_('File'), upload_to='employee_documents/')
    description = models.TextField(_('Description'), blank=True, null=True)
    expiry_date = models.DateField(_('Expiry Date'), blank=True, null=True)
    is_verified = models.BooleanField(_('Verified'), default=False)
    
    class Meta:
        verbose_name = _('Employee Document')
        verbose_name_plural = _('Employee Documents')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.title}"


class Attendance(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Employee attendance"""
    ATTENDANCE_STATUS_CHOICES = [
        ('present', _('Present')),
        ('absent', _('Absent')),
        ('late', _('Late')),
        ('early_leave', _('Early Leave')),
        ('leave', _('Leave')),
        ('holiday', _('Holiday')),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances', verbose_name=_('Employee'))
    
    date = models.DateField(_('Date'))
    status = models.CharField(_('Status'), max_length=20, choices=ATTENDANCE_STATUS_CHOICES)
    
    check_in = models.DateTimeField(_('Check In'), blank=True, null=True)
    check_out = models.DateTimeField(_('Check Out'), blank=True, null=True)
    
    late_minutes = models.PositiveIntegerField(_('Late Minutes'), default=0)
    early_leave_minutes = models.PositiveIntegerField(_('Early Leave Minutes'), default=0)
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendance')
        ordering = ['-date', 'employee__first_name']
        unique_together = [['organization', 'employee', 'date']]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['employee']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.status}"


class LeaveType(UUIDModel, TimeStampedModel):
    """Leave type"""
    name = models.CharField(_('Name'), max_length=100, unique=True)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    
    maximum_days = models.PositiveIntegerField(_('Maximum Days'), default=0)
    is_paid = models.BooleanField(_('Paid Leave'), default=True)
    requires_approval = models.BooleanField(_('Requires Approval'), default=True)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Leave Type')
        verbose_name_plural = _('Leave Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class LeaveRequest(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Leave request"""
    LEAVE_STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('submitted', _('Submitted')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests', verbose_name=_('Employee'))
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name='leave_requests', verbose_name=_('Leave Type'))
    
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    
    status = models.CharField(_('Status'), max_length=20, choices=LEAVE_STATUS_CHOICES, default='draft')
    
    reason = models.TextField(_('Reason'), blank=True, null=True)
    
    submitted_at = models.DateTimeField(_('Submitted At'), blank=True, null=True)
    approved_at = models.DateTimeField(_('Approved At'), blank=True, null=True)
    rejected_at = models.DateTimeField(_('Rejected At'), blank=True, null=True)
    
    submitted_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='submitted_leaves', verbose_name=_('Submitted By'))
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves', verbose_name=_('Approved By'))
    rejected_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_leaves', verbose_name=_('Rejected By'))
    
    rejection_reason = models.TextField(_('Rejection Reason'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Leave Request')
        verbose_name_plural = _('Leave Requests')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['leave_type']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date']),
        ]
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.name} - {self.start_date}"
    
    @property
    def days_requested(self):
        from django.utils import timezone
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0


class LeaveBalance(UUIDModel, TimeStampedModel):
    """Employee leave balance"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_balances', verbose_name=_('Employee'))
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name='employee_balances', verbose_name=_('Leave Type'))
    
    year = models.PositiveIntegerField(_('Year'))
    
    allocated_days = models.DecimalField(_('Allocated Days'), max_digits=5, decimal_places=1, default=0.0)
    used_days = models.DecimalField(_('Used Days'), max_digits=5, decimal_places=1, default=0.0)
    remaining_days = models.DecimalField(_('Remaining Days'), max_digits=5, decimal_places=1, default=0.0)
    
    class Meta:
        verbose_name = _('Leave Balance')
        verbose_name_plural = _('Leave Balances')
        ordering = ['-year', 'employee__first_name']
        unique_together = [['employee', 'leave_type', 'year']]
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type.name} - {self.year}"


class SalaryComponent(UUIDModel, TimeStampedModel):
    """Salary component"""
    COMPONENT_TYPE_CHOICES = [
        ('basic', _('Basic Salary')),
        ('allowance', _('Allowance')),
        ('deduction', _('Deduction')),
        ('bonus', _('Bonus')),
        ('commission', _('Commission')),
        ('overtime', _('Overtime')),
        ('tax', _('Tax')),
        ('insurance', _('Insurance')),
        ('other', _('Other')),
    ]
    
    name = models.CharField(_('Name'), max_length=100, unique=True)
    code = models.CharField(_('Code'), max_length=10, unique=True)
    component_type = models.CharField(_('Component Type'), max_length=20, choices=COMPONENT_TYPE_CHOICES)
    description = models.TextField(_('Description'), blank=True, null=True)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Salary Component')
        verbose_name_plural = _('Salary Components')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SalaryStructure(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Employee salary structure"""
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary_structure', verbose_name=_('Employee'))
    
    effective_date = models.DateField(_('Effective Date'))
    end_date = models.DateField(_('End Date'), blank=True, null=True)
    
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Salary Structure')
        verbose_name_plural = _('Salary Structures')
        ordering = ['-effective_date']
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.effective_date}"


class SalaryComponentValue(UUIDModel, TimeStampedModel):
    """Salary component values"""
    salary_structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name='component_values', verbose_name=_('Salary Structure'))
    component = models.ForeignKey(SalaryComponent, on_delete=models.PROTECT, related_name='salary_values', verbose_name=_('Component'))
    
    value_type = models.CharField(_('Value Type'), max_length=20, choices=[('fixed', 'Fixed'), ('percentage', 'Percentage'), ('formula', 'Formula')], default='fixed')
    fixed_value = CurrencyField(_('Fixed Value'), default=0.00)
    percentage_value = models.DecimalField(_('Percentage Value'), max_digits=5, decimal_places=2, default=0.00)
    formula = models.CharField(_('Formula'), max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Salary Component Value')
        verbose_name_plural = _('Salary Component Values')
        ordering = ['component__name']
        unique_together = [['salary_structure', 'component']]
    
    def __str__(self):
        return f"{self.salary_structure.employee.full_name} - {self.component.name}"


class Payroll(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Payroll"""
    PAYROLL_STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('calculated', _('Calculated')),
        ('approved', _('Approved')),
        ('paid', _('Paid')),
        ('cancelled', _('Cancelled')),
    ]
    
    payroll_number = models.CharField(_('Payroll Number'), max_length=50, unique=True)
    
    period_start = models.DateField(_('Period Start'))
    period_end = models.DateField(_('Period End'))
    
    status = models.CharField(_('Status'), max_length=20, choices=PAYROLL_STATUS_CHOICES, default='draft')
    
    total_gross = CurrencyField(_('Total Gross'), default=0.00)
    total_deductions = CurrencyField(_('Total Deductions'), default=0.00)
    total_net = CurrencyField(_('Total Net'), default=0.00)
    
    payment_date = models.DateField(_('Payment Date'), blank=True, null=True)
    
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_payrolls', verbose_name=_('Created By'))
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_payrolls', verbose_name=_('Approved By'))
    paid_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='paid_payrolls', verbose_name=_('Paid By'))
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Payroll')
        verbose_name_plural = _('Payrolls')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['payroll_number']),
            models.Index(fields=['period_start']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.payroll_number} - {self.period_start} to {self.period_end}"


class PayrollItem(UUIDModel, TimeStampedModel):
    """Items in a payroll"""
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='items', verbose_name=_('Payroll'))
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payroll_items', verbose_name=_('Employee'))
    
    basic_salary = CurrencyField(_('Basic Salary'), default=0.00)
    gross_salary = CurrencyField(_('Gross Salary'), default=0.00)
    
    total_allowances = CurrencyField(_('Total Allowances'), default=0.00)
    total_deductions = CurrencyField(_('Total Deductions'), default=0.00)
    net_salary = CurrencyField(_('Net Salary'), default=0.00)
    
    payment_method = models.ForeignKey('pos.PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True, related_name='payroll_items', verbose_name=_('Payment Method'))
    payment_reference = models.CharField(_('Payment Reference'), max_length=100, blank=True, null=True)
    
    is_paid = models.BooleanField(_('Paid'), default=False)
    paid_date = models.DateField(_('Paid Date'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Payroll Item')
        verbose_name_plural = _('Payroll Items')
        ordering = ['-created_at']
        unique_together = [['payroll', 'employee']]
    
    def __str__(self):
        return f"{self.payroll.payroll_number} - {self.employee.full_name}"


class PayrollComponent(UUIDModel, TimeStampedModel):
    """Components in a payroll item"""
    payroll_item = models.ForeignKey(PayrollItem, on_delete=models.CASCADE, related_name='components', verbose_name=_('Payroll Item'))
    component = models.ForeignKey(SalaryComponent, on_delete=models.PROTECT, related_name='payroll_components', verbose_name=_('Component'))
    
    amount = CurrencyField(_('Amount'), default=0.00)
    
    class Meta:
        verbose_name = _('Payroll Component')
        verbose_name_plural = _('Payroll Components')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.payroll_item} - {self.component.name}"


class Commission(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Employee commission"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='commissions', verbose_name=_('Employee'))
    
    period_start = models.DateField(_('Period Start'))
    period_end = models.DateField(_('Period End'))
    
    amount = CurrencyField(_('Amount'), default=0.00)
    percentage = models.DecimalField(_('Percentage'), max_digits=5, decimal_places=2, default=0.00)
    base_amount = CurrencyField(_('Base Amount'), default=0.00)
    
    reference = models.CharField(_('Reference'), max_length=100, blank=True, null=True)
    reference_type = models.CharField(_('Reference Type'), max_length=50, blank=True, null=True)
    
    is_paid = models.BooleanField(_('Paid'), default=False)
    paid_date = models.DateField(_('Paid Date'), blank=True, null=True)
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Commission')
        verbose_name_plural = _('Commissions')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['period_start']),
        ]
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.period_start} to {self.period_end}"


class Overtime(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """Employee overtime"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='overtimes', verbose_name=_('Employee'))
    
    date = models.DateField(_('Date'))
    hours = models.DecimalField(_('Hours'), max_digits=5, decimal_places=2, default=0.00)
    rate = CurrencyField(_('Rate'), default=0.00)
    amount = CurrencyField(_('Amount'), default=0.00)
    
    is_approved = models.BooleanField(_('Approved'), default=False)
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_overtimes', verbose_name=_('Approved By'))
    approved_at = models.DateTimeField(_('Approved At'), blank=True, null=True)
    
    is_paid = models.BooleanField(_('Paid'), default=False)
    paid_date = models.DateField(_('Paid Date'), blank=True, null=True)
    
    notes = models.TextField(_('Notes'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Overtime')
        verbose_name_plural = _('Overtimes')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.date} - {self.hours} hours"
    
    def save(self, *args, **kwargs):
        self.amount = self.hours * self.rate
        super().save(*args, **kwargs)


class HRReport(UUIDModel, TimeStampedModel, OrganizationAndBranchScopedModel):
    """HR report"""
    REPORT_TYPE_CHOICES = [
        ('employee_list', _('Employee List')),
        ('attendance_summary', _('Attendance Summary')),
        ('leave_summary', _('Leave Summary')),
        ('payroll_summary', _('Payroll Summary')),
        ('turnover', _('Turnover Report')),
        ('custom', _('Custom')),
    ]
    
    name = models.CharField(_('Name'), max_length=200)
    report_type = models.CharField(_('Report Type'), max_length=20, choices=REPORT_TYPE_CHOICES)
    
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'))
    
    parameters = models.JSONField(_('Parameters'), blank=True, null=True)
    data = models.JSONField(_('Data'), blank=True, null=True)
    
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_hr_reports', verbose_name=_('Generated By'))
    
    file = models.FileField(_('File'), upload_to='hr_reports/', blank=True, null=True)
    
    class Meta:
        verbose_name = _('HR Report')
        verbose_name_plural = _('HR Reports')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"
