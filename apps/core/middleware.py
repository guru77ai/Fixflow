"""
Middleware for organization and branch context resolution.
This middleware ensures that every request has access to the current organization and branch
and that the user has proper access to them.
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from apps.organizations.models import Organization, OrganizationMembership
from apps.branches.models import Branch, BranchUserAccess


class OrganizationContextMiddleware:
    """
    Middleware that resolves and validates the current organization for the request.
    
    Sets request.organization for use in views and API endpoints.
    Fails closed (redirect or 403) if no valid organization context exists.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.process_request(request)
        if response is not None:
            return response
        
        response = self.get_response(request)
        return response
    
    def process_request(self, request):
        """
        Resolve organization context from session and validate user membership.
        """
        # Skip for admin, API schema, JWT, and static/media URLs
        path = request.path
        skip_paths = [
            '/admin/', '/api/schema/', '/api/docs/',
            '/api/token/', '/api/token/refresh/',
            '/i18n/setlang/', '/static/', '/media/'
        ]
        
        for skip_path in skip_paths:
            if path.startswith(skip_path):
                return None
        
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return None
        
        # Get organization ID from session
        org_id = request.session.get('organization_id')
        
        if not org_id:
            # Try to set from first available organization
            membership = OrganizationMembership.objects.filter(
                user=request.user,
                is_active=True
            ).select_related('organization').first()
            
            if membership:
                request.session['organization_id'] = str(membership.organization.pk)
                request.organization = membership.organization
            else:
                # No organizations available - redirect to organization selection
                if not path.startswith('/accounts/') and not path.startswith('/api/'):
                    messages.error(request, "Please select an organization")
                    return redirect('organization_select')
            return None
        
        # Get and validate organization
        try:
            organization = Organization.objects.get(pk=org_id, is_active=True)
        except Organization.DoesNotExist:
            # Organization doesn't exist - clear session and redirect
            del request.session['organization_id']
            if not path.startswith('/accounts/') and not path.startswith('/api/'):
                messages.error(request, "Organization not found")
                return redirect('organization_select')
            return None
        
        # Validate user membership
        has_membership = OrganizationMembership.objects.filter(
            user=request.user,
            organization=organization,
            is_active=True
        ).exists()
        
        if not has_membership:
            # User doesn't have access to this organization
            del request.session['organization_id']
            if not path.startswith('/accounts/') and not path.startswith('/api/'):
                messages.error(request, "You do not have access to this organization")
                return redirect('organization_select')
            return None
        
        # Set organization on request
        request.organization = organization
        
        return None


class BranchContextMiddleware:
    """
    Middleware that resolves and validates the current branch for the request.
    
    Sets request.branch for use in views and API endpoints.
    Requires organization context to be set first.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.process_request(request)
        if response is not None:
            return response
        
        response = self.get_response(request)
        return response
    
    def process_request(self, request):
        """
        Resolve branch context from session and validate user access.
        """
        # Skip for admin, API schema, JWT, and static/media URLs
        path = request.path
        skip_paths = [
            '/admin/', '/api/schema/', '/api/docs/',
            '/api/token/', '/api/token/refresh/',
            '/i18n/setlang/', '/static/', '/media/'
        ]
        
        for skip_path in skip_paths:
            if path.startswith(skip_path):
                return None
        
        # Skip if user is not authenticated
        if not request.user.is_authenticated:
            return None
        
        # Skip if organization context is not set
        if not hasattr(request, 'organization') or not request.organization:
            return None
        
        # Get branch ID from session
        branch_id = request.session.get('branch_id')
        
        if not branch_id:
            # Try to set from first available branch for the organization
            branches = Branch.objects.filter(
                organization=request.organization,
                is_active=True
            ).order_by('code')
            
            if branches.exists():
                # Check if user has explicit access to any branch
                user_access_branches = BranchUserAccess.objects.filter(
                    user=request.user,
                    branch__in=branches,
                    is_active=True
                ).select_related('branch').order_by('branch__code')
                
                if user_access_branches.exists():
                    request.session['branch_id'] = str(user_access_branches.first().branch.pk)
                    request.branch = user_access_branches.first().branch
                else:
                    # Check if user is org admin - can access any branch
                    is_org_admin = OrganizationMembership.objects.filter(
                        user=request.user,
                        organization=request.organization,
                        is_active=True,
                        role__code__in=['admin', 'super_admin']
                    ).exists()
                    
                    if is_org_admin:
                        request.session['branch_id'] = str(branches.first().pk)
                        request.branch = branches.first()
                    else:
                        # No branch access - redirect to branch selection
                        if not path.startswith('/accounts/') and not path.startswith('/api/'):
                            messages.error(request, "Please select a branch")
                            return redirect('branch_select')
            else:
                # No branches for this organization
                if not path.startswith('/accounts/') and not path.startswith('/api/'):
                    messages.error(request, "No branches available for this organization")
                    return redirect('organization_select')
            return None
        
        # Get and validate branch
        try:
            branch = Branch.objects.get(
                pk=branch_id,
                organization=request.organization,
                is_active=True
            )
        except Branch.DoesNotExist:
            # Branch doesn't exist - clear session and retry
            del request.session['branch_id']
            return None
        
        # Validate user access to this branch
        has_access = BranchUserAccess.objects.filter(
            user=request.user,
            branch=branch,
            is_active=True
        ).exists()
        
        # Also check if user is an admin of the organization
        is_org_admin = OrganizationMembership.objects.filter(
            user=request.user,
            organization=request.organization,
            is_active=True,
            role__code__in=['admin', 'super_admin']
        ).exists()
        
        if not (has_access or is_org_admin):
            # User doesn't have access to this branch
            del request.session['branch_id']
            if not path.startswith('/accounts/') and not path.startswith('/api/'):
                messages.error(request, "You do not have access to this branch")
                return redirect('branch_select')
            return None
        
        # Set branch on request
        request.branch = branch
        
        return None
