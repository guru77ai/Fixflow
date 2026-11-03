"""
Settings application configuration.
"""
from django.apps import AppConfig


class SettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.settings'
    verbose_name = 'Settings'
    
    def ready(self):
        # Import and register signals
        import apps.settings.signals
