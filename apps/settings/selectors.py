"""
Selectors for the settings application.
"""
from .models import SystemSetting, OrganizationSetting, BranchSetting, UserSetting


class SettingsSelector:
    """
    Selector for settings queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_system_setting(self, pk):
        """
        Get a system setting by ID.
        """
        try:
            setting = SystemSetting.objects.get(pk=pk)
            return self.get_system_setting_data(setting)
        except SystemSetting.DoesNotExist:
            return None
    
    def get_system_settings(self, **filters):
        """
        Get a list of system settings.
        """
        queryset = SystemSetting.objects.all()
        
        # Apply filters
        if 'category_id' in filters:
            queryset = queryset.filter(category_id=filters['category_id'])
        
        if 'key' in filters:
            queryset = queryset.filter(key=filters['key'])
        
        if 'is_public' in filters:
            queryset = queryset.filter(is_public=filters['is_public'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                key__icontains=search
            )
        
        return [
            self.get_system_setting_data(setting) for setting in queryset.order_by('category__order', 'key')
        ]
    
    def get_system_setting_data(self, setting):
        """
        Get system setting data for responses.
        """
        return {
            'id': str(setting.id),
            'category': {
                'id': str(setting.category.id) if setting.category else None,
                'name': setting.category.name if setting.category else None,
                'code': setting.category.code if setting.category else None,
            } if setting.category else None,
            'key': setting.key,
            'value': setting.value,
            'value_type': setting.value_type,
            'value_display': self.get_value_display(setting),
            'description': setting.description,
            'is_editable': setting.is_editable,
            'is_public': setting.is_public,
            'created_at': setting.created_at,
            'updated_at': setting.updated_at,
        }
    
    def get_value_display(self, setting):
        """
        Get the display value for a setting based on its type.
        """
        if setting.value_type == 'boolean':
            return 'Yes' if setting.get_value() else 'No'
        elif setting.value_type == 'json':
            return '[JSON Data]'
        else:
            return setting.value
    
    def get_organization_setting(self, pk):
        """
        Get an organization setting by ID.
        """
        try:
            setting = OrganizationSetting.objects.get(pk=pk)
            
            # Check organization access
            if not self.has_organization_access(setting.organization_id):
                return None
            
            return self.get_organization_setting_data(setting)
        except OrganizationSetting.DoesNotExist:
            return None
    
    def get_organization_settings(self, organization_id, **filters):
        """
        Get a list of organization settings.
        """
        queryset = OrganizationSetting.objects.filter(organization_id=organization_id)
        
        # Check organization access
        if not self.has_organization_access(organization_id):
            return []
        
        # Apply filters
        if 'category_id' in filters:
            queryset = queryset.filter(category_id=filters['category_id'])
        
        if 'key' in filters:
            queryset = queryset.filter(key=filters['key'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                key__icontains=search
            )
        
        return [
            self.get_organization_setting_data(setting) for setting in queryset.order_by('category__order', 'key')
        ]
    
    def get_organization_setting_data(self, setting):
        """
        Get organization setting data for responses.
        """
        return {
            'id': str(setting.id),
            'organization': {
                'id': str(setting.organization.id),
                'name': setting.organization.name,
                'code': setting.organization.code,
            },
            'category': {
                'id': str(setting.category.id) if setting.category else None,
                'name': setting.category.name if setting.category else None,
                'code': setting.category.code if setting.category else None,
            } if setting.category else None,
            'key': setting.key,
            'value': setting.value,
            'value_type': setting.value_type,
            'value_display': self.get_value_display(setting),
            'description': setting.description,
            'created_at': setting.created_at,
            'updated_at': setting.updated_at,
        }
    
    def has_organization_access(self, organization_id):
        """
        Check if user has access to an organization.
        """
        if not self.user.is_authenticated:
            return False
        
        if self.user.is_superuser:
            return True
        
        from apps.organizations.models import OrganizationMembership
        return OrganizationMembership.objects.filter(
            organization_id=organization_id,
            user=self.user
        ).exists()
