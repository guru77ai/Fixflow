"""
DRF authentication classes for tenant context resolution.
These classes ensure that JWT-authenticated API requests have proper
organization and branch context set.
"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.conf import settings
from apps.organizations.models import Organization, OrganizationMembership
from apps.branches.models import Branch, BranchUserAccess


class TenantContextAuthentication(BaseAuthentication):
    """
    Authentication class that resolves tenant context for API requests.
    
    This class:
    1. Runs AFTER JWT authentication (ordered after JWT in DEFAULT_AUTHENTICATION_CLASSES)
    2. Resolves organization and branch from request headers, session, or user defaults
    3. Sets request.organization and request.branch for use in views
    4. Validates user membership and access
    
    Organization can be specified via:
    - Header: X-Organization-ID
    - Session: organization_id
    - User's default organization (first membership)
    
    Branch can be specified via:
    - Header: X-Branch-ID
    - Session: branch_id
    - User's default branch (first accessible branch in organization)
    """
    
    def authenticate(self, request):
        # Only process if user is already authenticated (JWT or Session)
        if not request.user or not request.user.is_authenticated:
            return None
        
        # Resolve organization context
        organization = self.resolve_organization(request)
        if not organization:
            # Cannot proceed without organization
            raise AuthenticationFailed("Organization context required")
        
        # Set organization on request
        request.organization = organization
        
        # Resolve branch context
        branch = self.resolve_branch(request, organization)
        if not branch:
            # Branch is optional for some operations
            request.branch = None
        else:
            request.branch = branch
        
        # Return None since we're not providing authentication, just context
        return None
    
    def resolve_organization(self, request):
        """
        Resolve the organization for this request.
        """
        # Try header first
        org_id = getattr(request, '_organization_id', None) or request.META.get('HTTP_X_ORGANIZATION_ID')
        if org_id:
            return self.get_and_validate_organization(request.user, org_id)
        
        # Try session
        if hasattr(request, 'session'):
            org_id = request.session.get('organization_id')
            if org_id:
                org = self.get_and_validate_organization(request.user, org_id)
                if org:
                    return org
        
        # Try user's first organization
        if request.user.is_authenticated:
            membership = OrganizationMembership.objects.filter(
                user=request.user,
                is_active=True
            ).select_related('organization').first()
            
            if membership:
                return membership.organization
        
        return None
    
    def resolve_branch(self, request, organization):
        """
        Resolve the branch for this request given the organization.
        """
        # Try header first
        branch_id = getattr(request, '_branch_id', None) or request.META.get('HTTP_X_BRANCH_ID')
        if branch_id:
            return self.get_and_validate_branch(request.user, organization, branch_id)
        
        # Try session
        if hasattr(request, 'session'):
            branch_id = request.session.get('branch_id')
            if branch_id:
                branch = self.get_and_validate_branch(request.user, organization, branch_id)
                if branch:
                    return branch
        
        # Try user's first accessible branch in this organization
        if request.user.is_authenticated:
            # Check if user is org admin with all branch access
            is_org_admin = OrganizationMembership.objects.filter(
                user=request.user,
                organization=organization,
                is_active=True,
                can_access_all_branches=True
            ).exists()
            
            if is_org_admin:
                # Return first active branch for this organization
                branch = Branch.objects.filter(
                    organization=organization,
                    is_active=True
                ).first()
                if branch:
                    return branch
            else:
                # Get first branch the user has explicit access to
                branch_access = BranchUserAccess.objects.filter(
                    user=request.user,
                    branch__organization=organization,
                    is_active=True,
                    can_access=True
                ).select_related('branch').first()
                
                if branch_access:
                    return branch_access.branch
        
        return None
    
    def get_and_validate_organization(self, user, org_id):
        """
        Get and validate organization access for a user.
        """
        try:
            organization = Organization.objects.get(pk=org_id, is_active=True)
        except Organization.DoesNotExist:
            return None
        
        # Validate user membership
        if not OrganizationMembership.objects.filter(
            organization=organization,
            user=user,
            is_active=True
        ).exists():
            raise PermissionDenied("You do not have access to this organization")
        
        return organization
    
    def get_and_validate_branch(self, user, organization, branch_id):
        """
        Get and validate branch access for a user in an organization.
        """
        try:
            branch = Branch.objects.get(
                pk=branch_id,
                organization=organization,
                is_active=True
            )
        except Branch.DoesNotExist:
            return None
        
        # Validate user access to this branch
        has_access = BranchUserAccess.objects.filter(
            user=user,
            branch=branch,
            is_active=True,
            can_access=True
        ).exists()
        
        # Also check if user is an admin of the organization
        is_org_admin = OrganizationMembership.objects.filter(
            user=user,
            organization=organization,
            is_active=True,
            can_access_all_branches=True
        ).exists()
        
        if not (has_access or is_org_admin):
            raise PermissionDenied("You do not have access to this branch")
        
        return branch
