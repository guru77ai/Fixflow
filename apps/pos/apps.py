"""
POS App Configuration for FixSoftRepair Pro
"""
from django.apps import AppConfig


class POSConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.pos'
    verbose_name = 'Point of Sale'

    def ready(self):
        import apps.pos.signals
