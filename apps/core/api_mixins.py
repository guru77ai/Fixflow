"""
API mixins for organization and branch context in DRF ViewSets.
These mixins ensure that API endpoints properly scope queries to the current tenant.
"""
from rest_framework import mixins as drf_mixins
from rest_framework.exceptions import PermissionDenied, NotFound
from django.core.exceptions import ObjectDoesNotExist


class OrganizationContextAPIMixin:
    """
    Mixin for DRF ViewSets that ensures organization context is available.
    
    This mixin:
    1. Verifies that request.organization exists and is valid
    2. Provides helper methods for scoping querysets
    3. Fails with 403 if organization context is missing
    """
    
    def get_organization(self):
        """
        Get the current organization from the request.
        Raises PermissionDenied if not available.
        """
        if not hasattr(self.request, 'organization') or not self.request.organization:
            raise PermissionDenied("Organization context required")
        return self.request.organization
    
    def get_organization_id(self):
        """
        Get the current organization ID from the request.
        """
        org = self.get_organization()
        return org.pk


class BranchContextAPIMixin:
    """
    Mixin for DRF ViewSets that ensures branch context is available.
    
    This mixin:
    1. Verifies that request.branch exists and is valid
    2. Provides helper methods for scoping querysets
    3. Fails with 403 if branch context is missing
    """
    
    def get_branch(self):
        """
        Get the current branch from the request.
        Raises PermissionDenied if not available.
        """
        if not hasattr(self.request, 'branch') or not self.request.branch:
            raise PermissionDenied("Branch context required")
        return self.request.branch
    
    def get_branch_id(self):
        """
        Get the current branch ID from the request.
        """
        branch = self.get_branch()
        return branch.pk


class TenantScopedMixin(OrganizationContextAPIMixin, BranchContextAPIMixin):
    """
    Mixin that provides tenant-scoping for ViewSets.
    
    This mixin:
    1. Requires both organization and branch context
    2. Provides methods to scope querysets to the current tenant
    3. Validates that objects belong to the current tenant
    """
    
    organization_field = 'organization'
    branch_field = 'branch'
    
    def get_queryset(self):
        """
        Base queryset method that should be overridden by subclasses.
        By default, returns the model's default queryset.
        Subclasses should call super().get_queryset() and then apply their filters.
        """
        # Return the base queryset from the ViewSet
        if hasattr(self, 'queryset') and self.queryset is not None:
            return self.queryset
        elif hasattr(self, 'model'):
            return self.model.objects.all()
        # Fallback to parent implementation
        if hasattr(super(), 'get_queryset'):
            return super().get_queryset()
        return self.model.objects.all() if hasattr(self, 'model') else self.queryset
    
    def filter_by_organization(self, queryset):
        """
        Filter a queryset by the current organization.
        """
        org = self.get_organization()
        if hasattr(queryset.model, self.organization_field):
            return queryset.filter(**{self.organization_field: org})
        return queryset
    
    def filter_by_branch(self, queryset):
        """
        Filter a queryset by the current branch.
        """
        branch = self.get_branch()
        if hasattr(queryset.model, self.branch_field):
            return queryset.filter(**{self.branch_field: branch})
        return queryset
    
    def filter_by_tenant(self, queryset):
        """
        Filter a queryset by both organization and branch.
        """
        return self.filter_by_organization(self.filter_by_branch(queryset))
    
    def validate_organization(self, obj):
        """
        Validate that an object belongs to the current organization.
        Raises PermissionDenied if not.
        """
        org = self.get_organization()
        if hasattr(obj, self.organization_field):
            org_field = getattr(obj, self.organization_field)
            if org_field and org_field.pk != org.pk:
                raise PermissionDenied("Object does not belong to current organization")
    
    def validate_branch(self, obj):
        """
        Validate that an object belongs to the current branch.
        Raises PermissionDenied if not.
        """
        branch = self.get_branch()
        if hasattr(obj, self.branch_field):
            branch_field = getattr(obj, self.branch_field)
            if branch_field and branch_field.pk != branch.pk:
                raise PermissionDenied("Object does not belong to current branch")
    
    def validate_tenant(self, obj):
        """
        Validate that an object belongs to both the current organization and branch.
        """
        self.validate_organization(obj)
        self.validate_branch(obj)
    
    def get_object(self):
        """
        Override get_object to validate tenant context.
        """
        obj = super().get_object()
        self.validate_tenant(obj)
        return obj


class TenantScopedModelViewSet(
    TenantScopedMixin,
    drf_mixins.CreateModelMixin,
    drf_mixins.RetrieveModelMixin,
    drf_mixins.UpdateModelMixin,
    drf_mixins.ListModelMixin,
    drf_mixins.DestroyModelMixin
):
    """
    Base ViewSet class that automatically scopes all operations to the current tenant.
    
    Subclasses should:
    1. Set queryset to the full queryset (e.g., Model.objects.all())
    2. Set serializer_class
    3. Override organization_field and/or branch_field if different from defaults
    4. The queryset will be automatically filtered by tenant in get_queryset()
    """
    
    def get_queryset(self):
        """
        Automatically filter queryset by tenant.
        """
        queryset = super().get_queryset()
        return self.filter_by_tenant(queryset)
    
    def perform_create(self, serializer):
        """
        Automatically set organization and branch for new objects.
        Validates that client cannot override tenant context.
        Always derives organization and branch from request context, never trusts client.
        """
        org = self.get_organization()
        branch = self.get_branch()
        
        # Validate that client-supplied organization/branch match the request context
        # If they don't match, raise PermissionDenied
        validated_data = serializer.validated_data
        
        # Check organization field - reject if client supplies any value
        # Client cannot override, set to null, or change organization
        if self.organization_field and self.organization_field in validated_data:
            client_org = validated_data[self.organization_field]
            # Reject if client supplies a different organization or tries to null it
            if client_org is None or (client_org and client_org.pk != org.pk):
                raise PermissionDenied("Cannot override organization context")
            # Remove from validated_data to prevent client from setting it
            del validated_data[self.organization_field]
        
        # Check branch field - reject if client supplies any value
        # Client cannot override, set to null, or change branch
        if self.branch_field and self.branch_field in validated_data:
            client_branch = validated_data[self.branch_field]
            # Reject if client supplies a different branch or tries to null it
            if client_branch is None or (client_branch and client_branch.pk != branch.pk):
                raise PermissionDenied("Cannot override branch context")
            # Remove from validated_data to prevent client from setting it
            del validated_data[self.branch_field]
        
        # Always save with organization and branch from request context
        save_kwargs = {}
        if self.organization_field:
            save_kwargs[self.organization_field] = org
        if self.branch_field:
            save_kwargs[self.branch_field] = branch
        
        serializer.save(**save_kwargs)


class TenantScopedReadOnlyModelViewSet(
    TenantScopedMixin,
    drf_mixins.RetrieveModelMixin,
    drf_mixins.ListModelMixin
):
    """
    Read-only ViewSet that automatically scopes queries to the current tenant.
    """
    
    def get_queryset(self):
        """
        Automatically filter queryset by tenant.
        """
        queryset = super().get_queryset()
        return self.filter_by_tenant(queryset)
