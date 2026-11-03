"""
Branches application configuration.
"""
from django.apps import AppConfig


class BranchesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.branches'
    verbose_name = 'Branches'
    
    def ready(self):
        # Import and register signals
        import apps.branches.signals
