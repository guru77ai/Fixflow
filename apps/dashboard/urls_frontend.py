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
    
    # Authentication
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('register/', accounts_views.register_view, name='register'),
    path('password-reset/', accounts_views.password_reset_view, name='password_reset'),
    path('password-reset/done/', accounts_views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', accounts_views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', accounts_views.password_reset_complete_view, name='password_reset_complete'),
    path('profile/', accounts_views.profile_view, name='profile'),
    path('settings/', accounts_views.settings_view, name='settings'),
    
    # Organizations
    path('organizations/', org_views.organization_list_view, name='organizations:list'),
    path('organizations/create/', org_views.organization_create_view, name='organizations:create'),
    path('organizations/<uuid:pk>/', org_views.organization_detail_view, name='organizations:detail'),
    path('organizations/<uuid:pk>/edit/', org_views.organization_edit_view, name='organizations:edit'),
    path('organizations/<uuid:pk>/delete/', org_views.organization_delete_view, name='organizations:delete'),
    
    # Branches
    path('branches/', branch_views.branch_list_view, name='branches:list'),
    path('branches/create/', branch_views.branch_create_view, name='branches:create'),
    path('branches/<uuid:pk>/', branch_views.branch_detail_view, name='branches:detail'),
    path('branches/<uuid:pk>/edit/', branch_views.branch_edit_view, name='branches:edit'),
    path('branches/<uuid:pk>/delete/', branch_views.branch_delete_view, name='branches:delete'),
    
    # Licensing
    path('license/', license_views.license_view, name='licensing:view'),
    
    # Audit Logs
    path('audit-logs/', audit_views.audit_log_list_view, name='audit_logs:list'),
    
    # Backups
    path('backups/', backup_views.backup_list_view, name='backups:list'),
    path('backups/create/', backup_views.backup_create_view, name='backups:create'),
    path('backups/<uuid:pk>/download/', backup_views.backup_download_view, name='backups:download'),
    path('backups/<uuid:pk>/delete/', backup_views.backup_delete_view, name='backups:delete'),
    
    # Notifications
    path('notifications/', notification_views.notification_list_view, name='notifications:list'),
    path('notifications/<uuid:pk>/', notification_views.notification_detail_view, name='notifications:detail'),
    
    # Zakat
    path('zakat/', zakat_views.zakat_calculator_view, name='zakat:calculator'),
    
    # Settings
    path('settings/general/', settings_views.general_settings_view, name='settings:general'),
    
    # Reports
    path('reports/', report_views.report_dashboard_view, name='reports:dashboard'),
    path('reports/sales/', report_views.sales_report_view, name='reports:sales'),
    path('reports/repairs/', report_views.repair_report_view, name='reports:repairs'),
    path('reports/inventory/', report_views.inventory_report_view, name='reports:inventory'),
    path('reports/financial/', report_views.financial_report_view, name='reports:financial'),
]
