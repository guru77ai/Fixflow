"""
API Views for HR module
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Department, Position, EmploymentType, Employee, EmployeeDocument,
    Attendance, LeaveType, LeaveRequest, LeaveBalance, SalaryComponent,
    SalaryStructure, SalaryComponentValue, Payroll, PayrollItem,
    PayrollComponent, Commission, Overtime, HRReport
)
from .serializers import (
    DepartmentSerializer, PositionSerializer, EmploymentTypeSerializer,
    EmployeeSerializer, EmployeeDocumentSerializer, AttendanceSerializer,
    LeaveTypeSerializer, LeaveRequestSerializer, LeaveBalanceSerializer,
    SalaryComponentSerializer, SalaryStructureSerializer,
    SalaryComponentValueSerializer, PayrollSerializer, PayrollItemSerializer,
    PayrollComponentSerializer, CommissionSerializer, OvertimeSerializer,
    HRReportSerializer
)
from apps.core.pagination import StandardResultsSetPagination
from apps.core.api_mixins import TenantScopedMixin


class DepartmentViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'manager', 'is_active']
    search_fields = ['name', 'code', 'description', 'manager__first_name', 'manager__last_name']
    ordering_fields = ['name', 'code', 'sequence']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class PositionViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'minimum_salary', 'maximum_salary']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class EmploymentTypeViewSet(viewsets.ModelViewSet):
    """Global reference data: not tenant-scoped"""
    queryset = EmploymentType.objects.all()
    serializer_class = EmploymentTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination


class EmployeeViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['position', 'department', 'employment_type', 'status', 'gender', 'is_active']
    search_fields = ['employee_number', 'first_name', 'last_name', 'email', 'phone', 'national_id']
    ordering_fields = ['employee_number', 'first_name', 'last_name', 'hire_date']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        employee = self.get_object()
        self.validate_tenant(employee)
        attendance = employee.attendance_records.all()
        serializer = AttendanceSerializer(attendance, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def leaves(self, request, pk=None):
        employee = self.get_object()
        self.validate_tenant(employee)
        leaves = employee.leave_requests.all()
        serializer = LeaveRequestSerializer(leaves, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def payrolls(self, request, pk=None):
        employee = self.get_object()
        self.validate_tenant(employee)
        payrolls = employee.payroll_records.all()
        serializer = PayrollSerializer(payrolls, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def overtimes(self, request, pk=None):
        employee = self.get_object()
        self.validate_tenant(employee)
        overtimes = employee.overtime_records.all()
        serializer = OvertimeSerializer(overtimes, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def commissions(self, request, pk=None):
        employee = self.get_object()
        self.validate_tenant(employee)
        commissions = employee.commissions.all()
        serializer = CommissionSerializer(commissions, many=True, context={'request': request})
        return Response(serializer.data)


class AttendanceViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'date', 'status']
    search_fields = ['employee__first_name', 'employee__last_name', 'notes']
    ordering_fields = ['date', 'check_in', 'created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class LeaveTypeViewSet(viewsets.ModelViewSet):
    """Global reference data: not tenant-scoped"""
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_paid', 'requires_approval', 'is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'maximum_days']
    pagination_class = StandardResultsSetPagination


class LeaveRequestViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'leave_type', 'status', 'start_date', 'end_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'reason']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave_request = self.get_object()
        self.validate_tenant(leave_request)
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
        leave_request.save()
        serializer = LeaveRequestSerializer(leave_request, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave_request = self.get_object()
        self.validate_tenant(leave_request)
        leave_request.status = 'rejected'
        leave_request.rejected_by = request.user
        leave_request.rejection_reason = request.data.get('reason', '')
        leave_request.save()
        serializer = LeaveRequestSerializer(leave_request, context={'request': request})
        return Response(serializer.data)


class LeaveBalanceViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch (via employee relationship)"""
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'leave_type', 'year']
    ordering_fields = ['employee__first_name', 'leave_type__name', 'year']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by tenant via employee relationship
        org = self.get_organization()
        branch = self.get_branch()
        return queryset.filter(
            employee__organization=org,
            employee__branch=branch
        ).distinct()


class PayrollViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'period_start', 'period_end', 'payment_date']
    search_fields = ['payroll_number', 'notes']
    ordering_fields = ['payroll_number', 'period_start', 'payment_date']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        payroll = self.get_object()
        self.validate_tenant(payroll)
        # Get employees from payroll items
        employees = Employee.objects.filter(
            payroll_items__payroll=payroll
        ).distinct()
        serializer = EmployeeSerializer(employees, many=True, context={'request': request})
        return Response(serializer.data)


class OvertimeViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Overtime.objects.all()
    serializer_class = OvertimeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'date', 'is_approved', 'is_paid']
    search_fields = ['employee__first_name', 'employee__last_name', 'notes']
    ordering_fields = ['date', 'hours', 'amount']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class CommissionViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'period_start', 'period_end', 'is_paid']
    search_fields = ['employee__first_name', 'employee__last_name', 'reference', 'notes']
    ordering_fields = ['period_start', 'amount']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class EmployeeDocumentViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch (via employee relationship)"""
    queryset = EmployeeDocument.objects.all()
    serializer_class = EmployeeDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'document_type']
    search_fields = ['employee__first_name', 'employee__last_name', 'name', 'description']
    ordering_fields = ['uploaded_at', 'name']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by tenant via employee relationship
        org = self.get_organization()
        branch = self.get_branch()
        return queryset.filter(
            employee__organization=org,
            employee__branch=branch
        ).distinct()


class SalaryComponentViewSet(viewsets.ModelViewSet):
    """Global reference data: not tenant-scoped"""
    queryset = SalaryComponent.objects.all()
    serializer_class = SalaryComponentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination


class SalaryStructureViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = SalaryStructure.objects.all()
    serializer_class = SalaryStructureSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())


class SalaryComponentValueViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch (via salary_structure relationship)"""
    queryset = SalaryComponentValue.objects.all()
    serializer_class = SalaryComponentValueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['salary_structure', 'salary_component']
    search_fields = ['salary_structure__name', 'salary_component__name']
    ordering_fields = ['salary_structure', 'salary_component', 'amount']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by tenant via salary_structure relationship
        org = self.get_organization()
        branch = self.get_branch()
        return queryset.filter(
            salary_structure__organization=org,
            salary_structure__branch=branch
        ).distinct()


class PayrollItemViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch (via payroll relationship)"""
    queryset = PayrollItem.objects.all()
    serializer_class = PayrollItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payroll', 'salary_component']
    search_fields = ['payroll__payroll_number', 'salary_component__name']
    ordering_fields = ['payroll', 'salary_component', 'amount']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by tenant via payroll relationship
        org = self.get_organization()
        branch = self.get_branch()
        return queryset.filter(
            payroll__organization=org,
            payroll__branch=branch
        ).distinct()


class PayrollComponentViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch (via payroll_item relationship)"""
    queryset = PayrollComponent.objects.all()
    serializer_class = PayrollComponentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payroll', 'salary_component']
    search_fields = ['payroll__payroll_number', 'salary_component__name']
    ordering_fields = ['payroll', 'salary_component', 'amount']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by tenant via payroll_item relationship
        org = self.get_organization()
        branch = self.get_branch()
        return queryset.filter(
            payroll_item__payroll__organization=org,
            payroll_item__payroll__branch=branch
        ).distinct()


class HRReportViewSet(TenantScopedMixin, viewsets.ModelViewSet):
    """Tenant-scoped: filtered by organization and branch"""
    queryset = HRReport.objects.all()
    serializer_class = HRReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'generated_by']
    search_fields = ['name', 'report_type']
    ordering_fields = ['name', 'generated_at']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return self.filter_by_tenant(super().get_queryset())
