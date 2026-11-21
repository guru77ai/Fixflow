"""
Frontend URLs for the dashboard application.
"""
from django.urls import path, include
from apps.accounts import views as accounts_views
from apps.organizations import views as org_views
from apps.branches import views as branch_views
from apps.licensing import views as license_views
from apps.audit_logs import views as audit_views
from apps.backups import views as backup_views
from apps.notifications import views as notification_views
from apps.zakat import views as zakat_views
from apps.settings import views as settings_views
from apps.reports import views as report_views
from . import views as dashboard_views

urlpatterns = [
    # Dashboard
    path('', dashboard_views.dashboard_view, name='dashboard'),
    
    # Authentication (moved to accounts.urls_frontend)
    # path('login/', accounts_views.login_view, name='login'),
    
    # Organization selection
    path('select-organization/', org_views.organization_select_view, name='organization_select'),
    
    # Organizations
    path('organizations/', org_views.organization_list_view, name='organization_list'),
    path('organizations/create/', org_views.organization_create_view, name='organization_create'),
    path('organizations/<uuid:pk>/', org_views.organization_detail_view, name='organization_detail'),
    path('organizations/<uuid:pk>/edit/', org_views.organization_edit_view, name='organization_edit'),
    path('organizations/<uuid:pk>/delete/', org_views.organization_delete_view, name='organization_delete'),
    
    # Branch selection
    path('select-branch/', branch_views.branch_select_view, name='branch_select'),
    
    # Branches
    path('branches/', branch_views.branch_list_view, name='branch_list'),
    path('branches/create/', branch_views.branch_create_view, name='branch_create'),
    path('branches/<uuid:pk>/', branch_views.branch_detail_view, name='branch_detail'),
    path('branches/<uuid:pk>/edit/', branch_views.branch_edit_view, name='branch_edit'),
    path('branches/<uuid:pk>/delete/', branch_views.branch_delete_view, name='branch_delete'),
    
    # Licensing
    path('license/', license_views.license_view, name='license_view'),
    
    # Audit Logs
    path('audit-logs/', audit_views.audit_log_list_view, name='audit_log_list'),
    
    # Backups
    path('backups/', backup_views.backup_list_view, name='backup_list'),
    path('backups/create/', backup_views.backup_create_view, name='backup_create'),
    path('backups/<uuid:pk>/download/', backup_views.backup_download_view, name='backup_download'),
    path('backups/<uuid:pk>/delete/', backup_views.backup_delete_view, name='backup_delete'),
    
    # Notifications
    path('notifications/', notification_views.notification_list_view, name='notification_list'),
    path('notifications/<uuid:pk>/', notification_views.notification_detail_view, name='notification_detail'),
    
    # Zakat
    path('zakat/', zakat_views.zakat_calculator_view, name='zakat_calculator'),
    
    # Settings
    path('settings/general/', settings_views.general_settings_view, name='general_settings'),
    
    # Reports
    path('reports/', report_views.report_dashboard_view, name='report_dashboard'),
    path('reports/sales/', report_views.sales_report_view, name='sales_report'),
    path('reports/repairs/', report_views.repair_report_view, name='repair_report'),
    path('reports/inventory/', report_views.inventory_report_view, name='inventory_report'),
    path('reports/financial/', report_views.financial_report_view, name='financial_report'),
]
