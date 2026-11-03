"""
Selectors for the organizations application.
"""
from django.db.models import Q
from .models import Organization, OrganizationMembership


class OrganizationSelector:
    """
    Selector for organization-related queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_organization(self, pk):
        """
        Get an organization by ID.
        """
        try:
            organization = Organization.objects.get(pk=pk)
            
            # Check access
            if not self.has_organization_access(organization):
                return None
            
            return self.get_organization_data(organization)
        except Organization.DoesNotExist:
            return None
    
    def get_organizations(self, **filters):
        """
        Get a list of organizations.
        """
        queryset = Organization.objects.all()
        
        # Apply filters based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all organizations
                pass
            else:
                # Regular users can only see their organizations
                memberships = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(id__in=memberships)
        else:
            # Anonymous users can't see any organizations
            queryset = queryset.none()
        
        # Apply additional filters
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(legal_name__icontains=search) |
                Q(code__icontains=search)
            )
        
        return [
            self.get_organization_data(org) for org in queryset.order_by('name')
        ]
    
    def has_organization_access(self, organization):
        """
        Check if user has access to an organization.
        """
        if not self.user.is_authenticated:
            return False
        
        if self.user.is_superuser:
            return True
        
        return OrganizationMembership.objects.filter(
            organization=organization,
            user=self.user
        ).exists()
    
    def get_organization_data(self, organization):
        """
        Get organization data for responses.
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
            'industry': organization.get_industry_display(),
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
            'license_expiry': organization.license_expiry,
            'notes': organization.notes,
            'is_active': organization.is_active,
            'created_at': organization.created_at,
            'updated_at': organization.updated_at,
        }
    
    def get_memberships(self, organization):
        """
        Get memberships for an organization.
        """
        if not self.has_organization_access(organization):
            return []
        
        memberships = OrganizationMembership.objects.filter(
            organization=organization
        ).select_related('user', 'role')
        
        return [
            {
                'id': str(m.id),
                'user': {
                    'id': str(m.user.id),
                    'email': m.user.email,
                    'username': m.user.username,
                    'first_name': m.user.first_name,
                    'last_name': m.user.last_name,
                },
                'role': {
                    'id': str(m.role.id) if m.role else None,
                    'name': m.role.name if m.role else None,
                } if m.role else None,
                'is_owner': m.is_owner,
                'is_admin': m.is_admin,
                'can_manage_users': m.can_manage_users,
                'can_manage_settings': m.can_manage_settings,
                'can_access_all_branches': m.can_access_all_branches,
                'created_at': m.created_at.isoformat(),
            }
            for m in memberships
        ]
