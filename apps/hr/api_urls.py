"""
API URLs for HR module
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    DepartmentViewSet, PositionViewSet, EmploymentTypeViewSet,
    EmployeeViewSet, AttendanceViewSet, LeaveTypeViewSet,
    LeaveRequestViewSet, LeaveBalanceViewSet, PayrollViewSet,
    OvertimeViewSet, CommissionViewSet, HolidayViewSet,
    ShiftViewSet, EmployeeDocumentViewSet
)

router = DefaultRouter()

router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'employment-types', EmploymentTypeViewSet, basename='employmenttype')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'leave-types', LeaveTypeViewSet, basename='leavetype')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leaverequest')
router.register(r'leave-balances', LeaveBalanceViewSet, basename='leavebalance')
router.register(r'payrolls', PayrollViewSet, basename='payroll')
router.register(r'overtime', OvertimeViewSet, basename='overtime')
router.register(r'commissions', CommissionViewSet, basename='commission')
router.register(r'holidays', HolidayViewSet, basename='holiday')
router.register(r'shifts', ShiftViewSet, basename='shift')
router.register(r'employee-documents', EmployeeDocumentViewSet, basename='employeedocument')

urlpatterns = [
    path('', include(router.urls)),
]
