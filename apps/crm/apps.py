"""
CRM App Configuration for FixSoftRepair Pro
"""
from django.apps import AppConfig


class CRMConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.crm'
    verbose_name = 'Customer Relationship Management'

    def ready(self):
        import apps.crm.signals
