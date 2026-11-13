"""
Mixins for organization and branch context resolution.
These mixins ensure that views have access to the current organization and branch
and that the user has proper access to them.
"""
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from apps.organizations.models import Organization, OrganizationMembership
from apps.branches.models import Branch, BranchUserAccess


class OrganizationContextMixin(AccessMixin):
    """
    Mixin that resolves and validates the current organization for the request.
    
    This mixin:
    1. Resolves the active organization from session
    2. Validates the user's membership in that organization
    3. Sets request.organization for use in views
    4. Fails closed (403 or redirect) if no valid organization context exists
    
    The organization can be specified via:
    - Session: request.session['organization_id']
    - URL parameter: self.organization_url_kwarg (default: 'organization_pk')
    - Query parameter: self.organization_url_kwarg
    
    Requires the user to be authenticated and have membership in the organization.
    """
    organization_url_kwarg = 'organization_pk'
    organization_url_param = 'organization_id'
    organization_session_key = 'organization_id'
    
    def get_organization_id(self):
        """
        Get the organization ID from URL kwarg, query param, or session.
        """
        # Try URL kwarg first
        org_id = self.kwargs.get(self.organization_url_kwarg)
        if org_id:
            return org_id
        
        # Try query parameter
        org_id = self.request.GET.get(self.organization_url_param)
        if org_id:
            return org_id
        
        # Try session
        org_id = self.request.session.get(self.organization_session_key)
        if org_id:
            return org_id
        
        return None
    
    def get_organization(self):
        """
        Get and validate the organization for this request.
        
        Returns the Organization instance if valid, None otherwise.
        Raises PermissionDenied if organization exists but user doesn't have access.
        """
        org_id = self.get_organization_id()
        if not org_id:
            return None
        
        try:
            organization = Organization.objects.get(pk=org_id, is_active=True)
        except Organization.DoesNotExist:
            return None
        
        # Validate user membership
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        
        # Check if user has membership in this organization
        has_membership = OrganizationMembership.objects.filter(
            user=self.request.user,
            organization=organization,
            is_active=True
        ).exists()
        
        if not has_membership:
            raise PermissionDenied("You do not have access to this organization")
        
        return organization
    
    def dispatch(self, request, *args, **kwargs):
        """
        Set the organization on the request before dispatching.
        """
        # First, let parent classes (like LoginRequiredMixin) do their checks
        response = super().dispatch(request, *args, **kwargs)
        
        # If parent returned a response (e.g., redirect to login), return it
        if response is not None:
            return response
        
        # Get and validate organization
        organization = self.get_organization()
        
        if organization is None:
            # No organization in session - try to set from first available
            if request.user.is_authenticated:
                membership = OrganizationMembership.objects.filter(
                    user=request.user,
                    is_active=True
                ).select_related('organization').first()
                
                if membership:
                    request.session[self.organization_session_key] = str(membership.organization.pk)
                    organization = membership.organization
                else:
                    # No organizations available - redirect to organization selection or deny
                    messages.error(request, "Please select an organization")
                    return redirect('organization_select')
            else:
                raise PermissionDenied("Authentication required")
        
        # Set organization on request for use in views
        request.organization = organization
        
        return super().dispatch(request, *args, **kwargs)


class BranchContextMixin(AccessMixin):
    """
    Mixin that resolves and validates the current branch for the request.
    
    This mixin:
    1. Resolves the active branch from session
    2. Validates the user's access to that branch
    3. Sets request.branch for use in views
    4. Fails closed (403 or redirect) if no valid branch context exists
    
    The branch can be specified via:
    - Session: request.session['branch_id']
    - URL parameter: self.branch_url_kwarg (default: 'branch_pk')
    - Query parameter: self.branch_url_param
    
    Requires the user to be authenticated, have organization context,
    and have access to the branch.
    """
    branch_url_kwarg = 'branch_pk'
    branch_url_param = 'branch_id'
    branch_session_key = 'branch_id'
    
    def get_branch_id(self):
        """
        Get the branch ID from URL kwarg, query param, or session.
        """
        # Try URL kwarg first
        branch_id = self.kwargs.get(self.branch_url_kwarg)
        if branch_id:
            return branch_id
        
        # Try query parameter
        branch_id = self.request.GET.get(self.branch_url_param)
        if branch_id:
            return branch_id
        
        # Try session
        branch_id = self.request.session.get(self.branch_session_key)
        if branch_id:
            return branch_id
        
        return None
    
    def get_branch(self):
        """
        Get and validate the branch for this request.
        
        Returns the Branch instance if valid, None otherwise.
        Raises PermissionDenied if branch exists but user doesn't have access.
        """
        # Must have organization context first
        if not hasattr(self.request, 'organization') and not self.request.organization:
            # Try to get organization from session
            org_id = self.request.session.get('organization_id')
            if org_id:
                try:
                    self.request.organization = Organization.objects.get(pk=org_id, is_active=True)
                except Organization.DoesNotExist:
                    self.request.organization = None
        
        if not hasattr(self.request, 'organization') or not self.request.organization:
            return None
        
        branch_id = self.get_branch_id()
        if not branch_id:
            return None
        
        try:
            branch = Branch.objects.get(
                pk=branch_id,
                organization=self.request.organization,
                is_active=True
            )
        except Branch.DoesNotExist:
            return None
        
        # Validate user access to this branch
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        
        # Check if user has access to this branch (either through BranchUserAccess or is org admin)
        has_access = BranchUserAccess.objects.filter(
            user=self.request.user,
            branch=branch,
            is_active=True
        ).exists()
        
        # Also check if user is an admin of the organization
        is_org_admin = OrganizationMembership.objects.filter(
            user=self.request.user,
            organization=self.request.organization,
            is_active=True,
            role__code__in=['admin', 'super_admin']
        ).exists()
        
        if not (has_access or is_org_admin):
            raise PermissionDenied("You do not have access to this branch")
        
        return branch
    
    def dispatch(self, request, *args, **kwargs):
        """
        Set the branch on the request before dispatching.
        """
        # First, let parent classes do their checks
        response = super().dispatch(request, *args, **kwargs)
        
        # If parent returned a response (e.g., redirect to login), return it
        if response is not None:
            return response
        
        # Get and validate branch
        branch = self.get_branch()
        
        if branch is None:
            # No branch in session - try to set from first available for the organization
            if hasattr(request, 'organization') and request.organization:
                # Get branches accessible to user
                accessible_branches = Branch.objects.filter(
                    organization=request.organization,
                    is_active=True
                ).order_by('code')
                
                if accessible_branches.exists():
                    # Check if user has explicit access to any branch
                    user_access_branches = BranchUserAccess.objects.filter(
                        user=request.user,
                        branch__in=accessible_branches,
                        is_active=True
                    ).select_related('branch').order_by('branch__code')
                    
                    if user_access_branches.exists():
                        request.session[self.branch_session_key] = str(user_access_branches.first().branch.pk)
                        branch = user_access_branches.first().branch
                    else:
                        # Check if user is org admin - can access any branch
                        is_org_admin = OrganizationMembership.objects.filter(
                            user=request.user,
                            organization=request.organization,
                            is_active=True,
                            role__code__in=['admin', 'super_admin']
                        ).exists()
                        
                        if is_org_admin:
                            request.session[self.branch_session_key] = str(accessible_branches.first().pk)
                            branch = accessible_branches.first()
                        else:
                            messages.error(request, "Please select a branch")
                            return redirect('branch_select')
                else:
                    messages.error(request, "No branches available for this organization")
                    return redirect('dashboard')
            else:
                raise PermissionDenied("Organization context required")
        
        # Set branch on request for use in views
        request.branch = branch
        
        return super().dispatch(request, *args, **kwargs)


class OrganizationAndBranchContextMixin(OrganizationContextMixin, BranchContextMixin):
    """
    Convenience mixin that combines both OrganizationContextMixin and BranchContextMixin.
    
    This ensures both organization and branch context are resolved and validated.
    """
    pass
