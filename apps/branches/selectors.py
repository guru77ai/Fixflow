"""
Selectors for the branches application.
"""
from django.db.models import Q
from .models import Branch, BranchUserAccess
from apps.organizations.models import Organization


class BranchSelector:
    """
    Selector for branch-related queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_branch(self, pk):
        """
        Get a branch by ID.
        """
        try:
            branch = Branch.objects.get(pk=pk)
            
            # Check access
            if not self.has_branch_access(branch):
                return None
            
            return self.get_branch_data(branch)
        except Branch.DoesNotExist:
            return None
    
    def get_branches(self, **filters):
        """
        Get a list of branches.
        """
        queryset = Branch.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all branches
                pass
            else:
                # Regular users can only see branches they have access to
                # Get organizations the user has access to
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                
                # Filter branches by those organizations
                queryset = queryset.filter(organization_id__in=org_ids)
                
                # Also filter by direct branch access
                branch_ids = BranchUserAccess.objects.filter(
                    user=self.user,
                    can_access=True
                ).values_list('branch', flat=True)
                
                queryset = queryset.filter(Q(id__in=branch_ids) | Q(organization_id__in=org_ids))
        else:
            # Anonymous users can't see any branches
            queryset = queryset.none()
        
        # Apply additional filters
        if 'organization_id' in filters:
            queryset = queryset.filter(organization_id=filters['organization_id'])
        
        if 'is_active' in filters:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if 'is_main_branch' in filters:
            queryset = queryset.filter(is_main_branch=filters['is_main_branch'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(organization__name__icontains=search)
            )
        
        return [
            self.get_branch_data(branch) for branch in queryset.order_by('organization__name', 'code')
        ]
    
    def has_branch_access(self, branch):
        """
        Check if user has access to a branch.
        """
        if not self.user.is_authenticated:
            return False
        
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
        Get branch data for responses.
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
            'is_main_branch': branch.is_main_branch,
            'is_active': branch.is_active,
            'created_at': branch.created_at,
            'updated_at': branch.updated_at,
        }
    
    def get_branch_access(self, branch):
        """
        Get user access information for a branch.
        """
        try:
            access = BranchUserAccess.objects.get(
                branch=branch,
                user=self.user
            )
            return {
                'id': str(access.id),
                'can_access': access.can_access,
                'can_manage': access.can_manage,
            }
        except BranchUserAccess.DoesNotExist:
            return None
