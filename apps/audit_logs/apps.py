"""
Audit Logs application configuration.
"""
from django.apps import AppConfig


class AuditLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.audit_logs'
    verbose_name = 'Audit Logs'
    
    def ready(self):
        # Import and register signals
        import apps.audit_logs.signals
