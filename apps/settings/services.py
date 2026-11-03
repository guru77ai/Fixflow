"""
Services for the settings application.
"""
from .models import SystemSetting, OrganizationSetting, BranchSetting, UserSetting


class SettingsService:
    """
    Service for settings operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def create_system_setting(self, data):
        """
        Create a new system setting.
        """
        if SystemSetting.objects.filter(key=data.get('key')).exists():
            return None
        
        setting = SystemSetting.objects.create(
            category_id=data.get('category_id'),
            key=data.get('key'),
            value=data.get('value'),
            value_type=data.get('value_type', 'string'),
            description=data.get('description', ''),
            is_editable=data.get('is_editable', True),
            is_public=data.get('is_public', False)
        )
        
        return self.get_system_setting_data(setting)
    
    def update_system_setting(self, pk, data):
        """
        Update a system setting.
        """
        try:
            setting = SystemSetting.objects.get(pk=pk)
            
            if 'value' in data:
                setting.value = data['value']
            if 'value_type' in data:
                setting.value_type = data['value_type']
            if 'description' in data:
                setting.description = data['description']
            if 'is_editable' in data:
                setting.is_editable = data['is_editable']
            if 'is_public' in data:
                setting.is_public = data['is_public']
            
            setting.save()
            
            return self.get_system_setting_data(setting)
        except SystemSetting.DoesNotExist:
            return None
    
    def delete_system_setting(self, pk):
        """
        Delete a system setting.
        """
        try:
            setting = SystemSetting.objects.get(pk=pk)
            setting.delete()
            return True
        except SystemSetting.DoesNotExist:
            return False
    
    def get_system_setting_data(self, setting):
        """
        Get system setting data for API responses.
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
            'description': setting.description,
            'is_editable': setting.is_editable,
            'is_public': setting.is_public,
            'created_at': setting.created_at.isoformat(),
            'updated_at': setting.updated_at.isoformat(),
        }
    
    def create_organization_setting(self, data):
        """
        Create a new organization setting.
        """
        organization_id = data.get('organization_id')
        
        # Check if user has access to the organization
        if not self.has_organization_access(organization_id):
            return None
        
        if OrganizationSetting.objects.filter(
            organization_id=organization_id,
            key=data.get('key')
        ).exists():
            return None
        
        setting = OrganizationSetting.objects.create(
            organization_id=organization_id,
            category_id=data.get('category_id'),
            key=data.get('key'),
            value=data.get('value'),
            value_type=data.get('value_type', 'string'),
            description=data.get('description', '')
        )
        
        return self.get_organization_setting_data(setting)
    
    def update_organization_setting(self, pk, data):
        """
        Update an organization setting.
        """
        try:
            setting = OrganizationSetting.objects.get(pk=pk)
            
            # Check permissions
            if not self.has_organization_access(setting.organization_id):
                return None
            
            if 'value' in data:
                setting.value = data['value']
            if 'value_type' in data:
                setting.value_type = data['value_type']
            if 'description' in data:
                setting.description = data['description']
            
            setting.save()
            
            return self.get_organization_setting_data(setting)
        except OrganizationSetting.DoesNotExist:
            return None
    
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
