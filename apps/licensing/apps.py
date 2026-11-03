"""
Licensing application configuration.
"""
from django.apps import AppConfig


class LicensingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.licensing'
    verbose_name = 'Licensing'
    
    def ready(self):
        # Import and register signals
        import apps.licensing.signals
