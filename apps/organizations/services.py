"""
Services for the organizations application.
"""
from .models import Organization, OrganizationMembership


class OrganizationService:
    """
    Service for organization-related operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def create_organization(self, data):
        """
        Create a new organization.
        """
        organization = Organization.objects.create(
            name=data.get('name'),
            legal_name=data.get('legal_name', ''),
            code=data.get('code'),
            logo=data.get('logo'),
            tax_identification_number=data.get('tax_identification_number'),
            tax_authority=data.get('tax_authority'),
            business_activity=data.get('business_activity'),
            industry=data.get('industry', 'gsm_repair'),
            currency=data.get('currency', 'DZD'),
            default_language=data.get('default_language', 'fr'),
            timezone=data.get('timezone', 'Africa/Algiers'),
            address=data.get('address', ''),
            city=data.get('city', ''),
            state=data.get('state', ''),
            postal_code=data.get('postal_code', ''),
            country=data.get('country', 'Algeria'),
            phone=data.get('phone', ''),
            secondary_phone=data.get('secondary_phone', ''),
            email=data.get('email', ''),
            website=data.get('website', ''),
            invoice_prefix=data.get('invoice_prefix', 'INV'),
            repair_prefix=data.get('repair_prefix', 'REP'),
            accounting_method=data.get('accounting_method', 'accrual'),
            fiscal_year_start=data.get('fiscal_year_start', '01'),
            notes=data.get('notes', ''),
            is_active=data.get('is_active', True)
        )
        
        # Create membership for current user
        OrganizationMembership.objects.create(
            organization=organization,
            user=self.user,
            is_owner=True,
            is_admin=True,
            can_manage_users=True,
            can_manage_settings=True,
            can_access_all_branches=True
        )
        
        return self.get_organization_data(organization)
    
    def update_organization(self, pk, data, partial=False):
        """
        Update an organization.
        """
        try:
            organization = Organization.objects.get(pk=pk)
            
            # Check permissions
            if not self.has_organization_access(organization):
                return None
            
            # Update fields
            if 'name' in data:
                organization.name = data['name']
            if 'legal_name' in data:
                organization.legal_name = data['legal_name']
            if 'code' in data:
                organization.code = data['code']
            if 'logo' in data:
                organization.logo = data['logo']
            if 'tax_identification_number' in data:
                organization.tax_identification_number = data['tax_identification_number']
            if 'tax_authority' in data:
                organization.tax_authority = data['tax_authority']
            if 'business_activity' in data:
                organization.business_activity = data['business_activity']
            if 'industry' in data:
                organization.industry = data['industry']
            if 'currency' in data:
                organization.currency = data['currency']
            if 'default_language' in data:
                organization.default_language = data['default_language']
            if 'timezone' in data:
                organization.timezone = data['timezone']
            if 'address' in data:
                organization.address = data['address']
            if 'city' in data:
                organization.city = data['city']
            if 'state' in data:
                organization.state = data['state']
            if 'postal_code' in data:
                organization.postal_code = data['postal_code']
            if 'country' in data:
                organization.country = data['country']
            if 'phone' in data:
                organization.phone = data['phone']
            if 'secondary_phone' in data:
                organization.secondary_phone = data['secondary_phone']
            if 'email' in data:
                organization.email = data['email']
            if 'website' in data:
                organization.website = data['website']
            if 'invoice_prefix' in data:
                organization.invoice_prefix = data['invoice_prefix']
            if 'repair_prefix' in data:
                organization.repair_prefix = data['repair_prefix']
            if 'accounting_method' in data:
                organization.accounting_method = data['accounting_method']
            if 'fiscal_year_start' in data:
                organization.fiscal_year_start = data['fiscal_year_start']
            if 'notes' in data:
                organization.notes = data['notes']
            if 'is_active' in data:
                organization.is_active = data['is_active']
            
            organization.save()
            
            return self.get_organization_data(organization)
        except Organization.DoesNotExist:
            return None
    
    def delete_organization(self, pk):
        """
        Delete an organization.
        """
        try:
            organization = Organization.objects.get(pk=pk)
            
            # Check permissions (must be owner)
            membership = OrganizationMembership.objects.filter(
                organization=organization,
                user=self.user,
                is_owner=True
            ).exists()
            
            if not membership:
                return False
            
            # Soft delete
            organization.is_active = False
            organization.save()
            
            return True
        except Organization.DoesNotExist:
            return False
    
    def has_organization_access(self, organization):
        """
        Check if user has access to an organization.
        """
        return OrganizationMembership.objects.filter(
            organization=organization,
            user=self.user
        ).exists()
    
    def get_organization_data(self, organization):
        """
        Get organization data for API responses.
        """
        return {
            'id': str(organization.id),
            'name': organization.name,
            'legal_name': organization.legal_name,
            'code': organization.code,
            'logo': organization.logo.url if organization.logo else None,
            'tax_identification_number': organization.tax_identification_number,
            'tax_authority': organization.tax_authority,
            'business_activity': organization.business_activity,
            'industry': organization.industry,
            'currency': organization.currency,
            'default_language': organization.default_language,
            'timezone': organization.timezone,
            'address': organization.address,
            'city': organization.city,
            'state': organization.state,
            'postal_code': organization.postal_code,
            'country': organization.country,
            'phone': organization.phone,
            'secondary_phone': organization.secondary_phone,
            'email': organization.email,
            'website': organization.website,
            'invoice_prefix': organization.invoice_prefix,
            'repair_prefix': organization.repair_prefix,
            'next_invoice_number': organization.next_invoice_number,
            'next_repair_number': organization.next_repair_number,
            'accounting_method': organization.accounting_method,
            'fiscal_year_start': organization.fiscal_year_start,
            'license_id': organization.license_id,
            'license_expiry': organization.license_expiry.isoformat() if organization.license_expiry else None,
            'notes': organization.notes,
            'is_active': organization.is_active,
            'created_at': organization.created_at.isoformat(),
            'updated_at': organization.updated_at.isoformat(),
        }
