"""
Suppliers App Configuration for FixSoftRepair Pro
"""
from django.apps import AppConfig


class SuppliersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.suppliers'
    verbose_name = 'Supplier Management'

    def ready(self):
        import apps.suppliers.signals
