"""
Selectors for the licensing application.
"""
from .models import License, Installation


class LicenseSelector:
    """
    Selector for license-related queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_license(self):
        """
        Get the license for the current organization.
        """
        # In a real implementation, this would be associated with the organization
        # For now, we'll just get the first active license
        try:
            license_obj = License.objects.filter(
                is_active=True
            ).order_by('-issue_date').first()
            
            if license_obj:
                return self.get_license_data(license_obj)
        except Exception:
            pass
        
        return None
    
    def get_license_by_id(self, license_id):
        """
        Get a license by ID.
        """
        try:
            license_obj = License.objects.get(license_id=license_id)
            return self.get_license_data(license_obj)
        except License.DoesNotExist:
            return None
    
    def get_installations(self, license_id=None):
        """
        Get installations.
        """
        queryset = Installation.objects.all()
        
        if license_id:
            queryset = queryset.filter(license__license_id=license_id)
        
        return [
            self.get_installation_data(inst) for inst in queryset.order_by('-created_at')
        ]
    
    def get_license_data(self, license_obj):
        """
        Get license data for responses.
        """
        return {
            'id': str(license_obj.id),
            'license_id': license_obj.license_id,
            'customer_name': license_obj.customer_name,
            'customer_email': license_obj.customer_email,
            'customer_phone': license_obj.customer_phone,
            'edition': license_obj.get_edition_display(),
            'enabled_modules': license_obj.enabled_modules,
            'issue_date': license_obj.issue_date,
            'expiry_date': license_obj.expiry_date,
            'installation_binding': license_obj.get_installation_binding_display(),
            'bound_to': license_obj.bound_to,
            'max_installations': license_obj.max_installations,
            'status': license_obj.get_status_display(),
            'status_reason': license_obj.status_reason,
            'maintenance_expires': license_obj.maintenance_expires,
            'can_upgrade': license_obj.can_upgrade,
            'notes': license_obj.notes,
            'is_active': license_obj.is_active,
            'is_perpetual': license_obj.is_perpetual(),
            'is_expired': license_obj.is_expired(),
            'is_valid': license_obj.is_valid(),
            'created_at': license_obj.created_at,
            'updated_at': license_obj.updated_at,
        }
    
    def get_installation_data(self, installation):
        """
        Get installation data for responses.
        """
        return {
            'id': str(installation.id),
            'license_id': installation.license.license_id,
            'installation_id': installation.installation_id,
            'machine_name': installation.machine_name,
            'machine_id': installation.machine_id,
            'mac_address': installation.mac_address,
            'hardware_id': installation.hardware_id,
            'ip_address': installation.ip_address,
            'is_active': installation.is_active,
            'last_active': installation.last_active,
            'created_at': installation.created_at,
        }
