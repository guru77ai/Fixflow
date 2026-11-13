"""
API URLs for HR module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    DepartmentViewSet, PositionViewSet, EmploymentTypeViewSet,
    EmployeeViewSet, EmployeeDocumentViewSet, AttendanceViewSet,
    LeaveTypeViewSet, LeaveRequestViewSet, LeaveBalanceViewSet,
    SalaryComponentViewSet, SalaryStructureViewSet,
    SalaryComponentValueViewSet, PayrollViewSet, PayrollItemViewSet,
    PayrollComponentViewSet, CommissionViewSet, OvertimeViewSet,
    HRReportViewSet
)

router = DefaultRouter()

router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'employment-types', EmploymentTypeViewSet, basename='employmenttype')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'employee-documents', EmployeeDocumentViewSet, basename='employeedocument')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'leave-types', LeaveTypeViewSet, basename='leavetype')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leaverequest')
router.register(r'leave-balances', LeaveBalanceViewSet, basename='leavebalance')
router.register(r'salary-components', SalaryComponentViewSet, basename='salarycomponent')
router.register(r'salary-structures', SalaryStructureViewSet, basename='salarystructure')
router.register(r'salary-component-values', SalaryComponentValueViewSet, basename='salarycomponentvalue')
router.register(r'payrolls', PayrollViewSet, basename='payroll')
router.register(r'payroll-items', PayrollItemViewSet, basename='payrollitem')
router.register(r'payroll-components', PayrollComponentViewSet, basename='payrollcomponent')
router.register(r'commissions', CommissionViewSet, basename='commission')
router.register(r'overtime', OvertimeViewSet, basename='overtime')
router.register(r'hr-reports', HRReportViewSet, basename='hrreport')

urlpatterns = [
    path('', include(router.urls)),
]
