"""
Repair App Configuration for FixSoftRepair Pro
"""
from django.apps import AppConfig


class RepairConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.repair'
    verbose_name = 'Repair Management'

    def ready(self):
        import apps.repair.signals
