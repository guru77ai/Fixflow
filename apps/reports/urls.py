"""
URLs for the reports application.
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # API URLs
    path('dashboard/', views.ReportDashboardAPIView.as_view(), name='api_dashboard'),
    path('sales/', views.SalesReportAPIView.as_view(), name='api_sales'),
    path('repairs/', views.RepairReportAPIView.as_view(), name='api_repairs'),
    path('inventory/', views.InventoryReportAPIView.as_view(), name='api_inventory'),
    path('financial/', views.FinancialReportAPIView.as_view(), name='api_financial'),
]
