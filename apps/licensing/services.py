"""
Services for the licensing application.
"""
import json
import hashlib
from django.conf import settings
from django.utils import timezone
from .models import License, LicenseVerificationLog, Installation


class LicenseService:
    """
    Service for license verification and management.
    """
    
    def __init__(self):
        self.public_key_path = settings.LICENSE_PUBLIC_KEY_PATH
    
    def verify_license(self, license_id, signature):
        """
        Verify a license using asymmetric cryptography.
        """
        try:
            # In a real implementation, we would use the public key to verify
            # the signature against the license data.
            # For this demo, we'll use a simple hash-based verification.
            
            # Get the license from database or create a mock one
            try:
                license_obj = License.objects.get(license_id=license_id)
            except License.DoesNotExist:
                return {
                    'valid': False,
                    'error': 'License not found'
                }
            
            # Verify the signature (simplified for demo)
            expected_signature = self.generate_signature(license_id, license_obj.customer_name)
            
            if signature != expected_signature:
                return {
                    'valid': False,
                    'error': 'Invalid signature'
                }
            
            # Check license status
            if not license_obj.is_active:
                return {
                    'valid': False,
                    'error': 'License is inactive'
                }
            
            if license_obj.is_expired():
                return {
                    'valid': False,
                    'error': 'License has expired'
                }
            
            # Log verification
            LicenseVerificationLog.objects.create(
                license=license_obj,
                license_id=license_id,
                is_valid=True,
                ip_address='',
                user_agent=''
            )
            
            return {
                'valid': True,
                'license': self.get_license_data(license_obj),
                'message': 'License is valid'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def generate_signature(self, license_id, customer_name):
        """
        Generate a signature for a license (simplified for demo).
        In a real implementation, this would use the private key.
        """
        data = f"{license_id}:{customer_name}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def create_license(self, data):
        """
        Create a new license (for internal use only, not exposed to users).
        """
        license_obj = License.objects.create(
            license_id=data.get('license_id'),
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            customer_phone=data.get('customer_phone'),
            edition=data.get('edition', 'professional'),
            enabled_modules=data.get('enabled_modules', []),
            issue_date=data.get('issue_date', timezone.now().date()),
            expiry_date=data.get('expiry_date'),
            installation_binding=data.get('installation_binding', 'none'),
            bound_to=data.get('bound_to'),
            max_installations=data.get('max_installations', 1),
            status=data.get('status', 'active'),
            status_reason=data.get('status_reason'),
            maintenance_expires=data.get('maintenance_expires'),
            can_upgrade=data.get('can_upgrade', True),
            notes=data.get('notes', ''),
            is_active=data.get('is_active', True)
        )
        
        # Generate signature
        signature = self.generate_signature(license_obj.license_id, license_obj.customer_name)
        license_obj.signature = signature
        license_obj.signed_data = json.dumps({
            'license_id': license_obj.license_id,
            'customer_name': license_obj.customer_name,
            'edition': license_obj.edition,
            'issue_date': license_obj.issue_date.isoformat(),
            'expiry_date': license_obj.expiry_date.isoformat() if license_obj.expiry_date else None,
        })
        license_obj.save()
        
        return self.get_license_data(license_obj)
    
    def create_installation(self, data):
        """
        Create a new installation record.
        """
        try:
            license_obj = License.objects.get(license_id=data.get('license_id'))
        except License.DoesNotExist:
            return None
        
        installation = Installation.objects.create(
            license=license_obj,
            installation_id=data.get('installation_id'),
            machine_name=data.get('machine_name'),
            machine_id=data.get('machine_id'),
            mac_address=data.get('mac_address'),
            hardware_id=data.get('hardware_id'),
            ip_address=data.get('ip_address'),
            is_active=data.get('is_active', True)
        )
        
        return self.get_installation_data(installation)
    
    def get_license_data(self, license_obj):
        """
        Get license data for API responses.
        """
        return {
            'id': str(license_obj.id),
            'license_id': license_obj.license_id,
            'customer_name': license_obj.customer_name,
            'customer_email': license_obj.customer_email,
            'customer_phone': license_obj.customer_phone,
            'edition': license_obj.edition,
            'enabled_modules': license_obj.enabled_modules,
            'issue_date': license_obj.issue_date.isoformat(),
            'expiry_date': license_obj.expiry_date.isoformat() if license_obj.expiry_date else None,
            'installation_binding': license_obj.installation_binding,
            'bound_to': license_obj.bound_to,
            'max_installations': license_obj.max_installations,
            'status': license_obj.status,
            'status_reason': license_obj.status_reason,
            'maintenance_expires': license_obj.maintenance_expires.isoformat() if license_obj.maintenance_expires else None,
            'can_upgrade': license_obj.can_upgrade,
            'notes': license_obj.notes,
            'is_active': license_obj.is_active,
            'is_perpetual': license_obj.is_perpetual(),
            'is_expired': license_obj.is_expired(),
            'is_valid': license_obj.is_valid(),
            'created_at': license_obj.created_at.isoformat(),
            'updated_at': license_obj.updated_at.isoformat(),
        }
    
    def get_installation_data(self, installation):
        """
        Get installation data for API responses.
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
            'last_active': installation.last_active.isoformat() if installation.last_active else None,
            'created_at': installation.created_at.isoformat(),
        }
