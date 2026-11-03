"""
Services for the branches application.
"""
from .models import Branch, BranchUserAccess
from apps.organizations.models import Organization


class BranchService:
    """
    Service for branch-related operations.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def create_branch(self, data):
        """
        Create a new branch.
        """
        organization_id = data.get('organization_id')
        
        # Check if user has access to the organization
        if not self.has_organization_access(organization_id):
            return None
        
        organization = Organization.objects.get(pk=organization_id)
        
        branch = Branch.objects.create(
            organization=organization,
            code=data.get('code'),
            name=data.get('name'),
            address=data.get('address', ''),
            city=data.get('city', ''),
            state=data.get('state', ''),
            postal_code=data.get('postal_code', ''),
            country=data.get('country', 'Algeria'),
            phone=data.get('phone', ''),
            secondary_phone=data.get('secondary_phone', ''),
            email=data.get('email', ''),
            website=data.get('website', ''),
            manager_id=data.get('manager_id'),
            is_main_branch=data.get('is_main_branch', False),
            auto_generate_documents=data.get('auto_generate_documents', True),
            next_sale_number=data.get('next_sale_number', 1),
            next_repair_number=data.get('next_repair_number', 1),
            next_purchase_number=data.get('next_purchase_number', 1),
            notes=data.get('notes', ''),
            is_active=data.get('is_active', True)
        )
        
        return self.get_branch_data(branch)
    
    def update_branch(self, pk, data, partial=False):
        """
        Update a branch.
        """
        try:
            branch = Branch.objects.get(pk=pk)
            
            # Check permissions
            if not self.has_branch_access(branch):
                return None
            
            # Update fields
            if 'code' in data:
                branch.code = data['code']
            if 'name' in data:
                branch.name = data['name']
            if 'address' in data:
                branch.address = data['address']
            if 'city' in data:
                branch.city = data['city']
            if 'state' in data:
                branch.state = data['state']
            if 'postal_code' in data:
                branch.postal_code = data['postal_code']
            if 'country' in data:
                branch.country = data['country']
            if 'phone' in data:
                branch.phone = data['phone']
            if 'secondary_phone' in data:
                branch.secondary_phone = data['secondary_phone']
            if 'email' in data:
                branch.email = data['email']
            if 'website' in data:
                branch.website = data['website']
            if 'manager_id' in data:
                branch.manager_id = data['manager_id']
            if 'is_main_branch' in data:
                branch.is_main_branch = data['is_main_branch']
            if 'auto_generate_documents' in data:
                branch.auto_generate_documents = data['auto_generate_documents']
            if 'notes' in data:
                branch.notes = data['notes']
            if 'is_active' in data:
                branch.is_active = data['is_active']
            
            branch.save()
            
            return self.get_branch_data(branch)
        except Branch.DoesNotExist:
            return None
    
    def delete_branch(self, pk):
        """
        Delete a branch.
        """
        try:
            branch = Branch.objects.get(pk=pk)
            
            # Check permissions
            if not self.has_branch_access(branch):
                return False
            
            # Soft delete
            branch.is_active = False
            branch.save()
            
            return True
        except Branch.DoesNotExist:
            return False
    
    def has_organization_access(self, organization_id):
        """
        Check if user has access to an organization.
        """
        from apps.organizations.models import OrganizationMembership
        
        if self.user.is_superuser:
            return True
        
        return OrganizationMembership.objects.filter(
            organization_id=organization_id,
            user=self.user
        ).exists()
    
    def has_branch_access(self, branch):
        """
        Check if user has access to a branch.
        """
        if self.user.is_superuser:
            return True
        
        # Check direct branch access
        if BranchUserAccess.objects.filter(
            branch=branch,
            user=self.user,
            can_access=True
        ).exists():
            return True
        
        # Check organization membership with all branch access
        from apps.organizations.models import OrganizationMembership
        return OrganizationMembership.objects.filter(
            organization=branch.organization,
            user=self.user,
            can_access_all_branches=True
        ).exists()
    
    def get_branch_data(self, branch):
        """
        Get branch data for API responses.
        """
        return {
            'id': str(branch.id),
            'organization': {
                'id': str(branch.organization.id),
                'name': branch.organization.name,
                'code': branch.organization.code,
            },
            'code': branch.code,
            'name': branch.name,
            'address': branch.address,
            'city': branch.city,
            'state': branch.state,
            'postal_code': branch.postal_code,
            'country': branch.country,
            'phone': branch.phone,
            'secondary_phone': branch.secondary_phone,
            'email': branch.email,
            'website': branch.website,
            'manager': {
                'id': str(branch.manager.id) if branch.manager else None,
                'email': branch.manager.email if branch.manager else None,
                'username': branch.manager.username if branch.manager else None,
                'first_name': branch.manager.first_name if branch.manager else None,
                'last_name': branch.manager.last_name if branch.manager else None,
            } if branch.manager else None,
            'warehouse': {
                'id': str(branch.warehouse.id) if branch.warehouse else None,
                'name': branch.warehouse.name if branch.warehouse else None,
                'code': branch.warehouse.code if branch.warehouse else None,
            } if branch.warehouse else None,
            'is_main_branch': branch.is_main_branch,
            'auto_generate_documents': branch.auto_generate_documents,
            'next_sale_number': branch.next_sale_number,
            'next_repair_number': branch.next_repair_number,
            'next_purchase_number': branch.next_purchase_number,
            'notes': branch.notes,
            'is_active': branch.is_active,
            'created_at': branch.created_at.isoformat(),
            'updated_at': branch.updated_at.isoformat(),
        }
