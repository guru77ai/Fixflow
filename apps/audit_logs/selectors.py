"""
Selectors for the audit_logs application.
"""
from django.db.models import Q
from .models import AuditLog, FinancialAuditLog


class AuditLogSelector:
    """
    Selector for audit log queries.
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
    
    def get_audit_log(self, pk):
        """
        Get an audit log by ID.
        """
        try:
            log = AuditLog.objects.get(pk=pk)
            
            # Check organization access
            if log.organization and not self.has_organization_access(log.organization):
                return None
            
            return self.get_audit_log_data(log)
        except AuditLog.DoesNotExist:
            return None
    
    def get_audit_logs(self, **filters):
        """
        Get a list of audit logs.
        """
        queryset = AuditLog.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all audit logs
                pass
            else:
                # Regular users can only see audit logs for their organizations
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(organization_id__in=org_ids)
        else:
            # Anonymous users can't see any audit logs
            queryset = queryset.none()
        
        # Apply additional filters
        if 'action' in filters:
            queryset = queryset.filter(action=filters['action'])
        
        if 'entity_type' in filters:
            queryset = queryset.filter(entity_type=filters['entity_type'])
        
        if 'user_id' in filters:
            queryset = queryset.filter(user_id=filters['user_id'])
        
        if 'organization_id' in filters:
            queryset = queryset.filter(organization_id=filters['organization_id'])
        
        if 'branch_id' in filters:
            queryset = queryset.filter(branch_id=filters['branch_id'])
        
        if 'start_date' in filters:
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        
        if 'end_date' in filters:
            queryset = queryset.filter(created_at__lte=filters['end_date'])
        
        if 'search' in filters and filters['search']:
            search = filters['search']
            queryset = queryset.filter(
                Q(action__icontains=search) |
                Q(entity_type__icontains=search) |
                Q(entity_repr__icontains=search) |
                Q(user__email__icontains=search)
            )
        
        return [
            self.get_audit_log_data(log) for log in queryset.order_by('-created_at')[:100]
        ]
    
    def has_organization_access(self, organization):
        """
        Check if user has access to an organization.
        """
        if not self.user.is_authenticated:
            return False
        
        if self.user.is_superuser:
            return True
        
        from apps.organizations.models import OrganizationMembership
        return OrganizationMembership.objects.filter(
            organization=organization,
            user=self.user
        ).exists()
    
    def get_audit_log_data(self, log):
        """
        Get audit log data for responses.
        """
        return {
            'id': str(log.id),
            'action': log.action,
            'action_display': log.get_action_display(),
            'user': {
                'id': str(log.user.id) if log.user else None,
                'email': log.user.email if log.user else None,
                'username': log.user.username if log.user else None,
            } if log.user else None,
            'user_email': log.user_email,
            'entity_type': log.entity_type,
            'entity_id': str(log.entity_id) if log.entity_id else None,
            'entity_repr': log.entity_repr,
            'organization': {
                'id': str(log.organization.id) if log.organization else None,
                'name': log.organization.name if log.organization else None,
            } if log.organization else None,
            'branch': {
                'id': str(log.branch.id) if log.branch else None,
                'name': log.branch.name if log.branch else None,
            } if log.branch else None,
            'ip_address': log.ip_address,
            'user_agent': log.user_agent,
            'request_path': log.request_path,
            'old_values': log.old_values,
            'new_values': log.new_values,
            'changed_fields': log.changed_fields,
            'notes': log.notes,
            'is_successful': log.is_successful,
            'error_message': log.error_message,
            'created_at': log.created_at.isoformat(),
        }
    
    def get_financial_audit_logs(self, **filters):
        """
        Get a list of financial audit logs.
        """
        queryset = FinancialAuditLog.objects.all()
        
        # Apply organization filter based on user access
        if self.user.is_authenticated:
            if self.user.is_superuser:
                # Superusers can see all financial audit logs
                pass
            else:
                # Regular users can only see financial audit logs for their organizations
                from apps.organizations.models import OrganizationMembership
                org_ids = OrganizationMembership.objects.filter(
                    user=self.user
                ).values_list('organization', flat=True)
                queryset = queryset.filter(organization_id__in=org_ids)
        else:
            # Anonymous users can't see any financial audit logs
            queryset = queryset.none()
        
        # Apply additional filters
        if 'operation' in filters:
            queryset = queryset.filter(operation=filters['operation'])
        
        if 'start_date' in filters:
            queryset = queryset.filter(created_at__gte=filters['start_date'])
        
        if 'end_date' in filters:
            queryset = queryset.filter(created_at__lte=filters['end_date'])
        
        return [
            self.get_financial_audit_log_data(log) for log in queryset.order_by('-created_at')[:100]
        ]
    
    def get_financial_audit_log_data(self, log):
        """
        Get financial audit log data for responses.
        """
        return {
            'id': str(log.id),
            'operation': log.operation,
            'operation_display': log.get_operation_display(),
            'user': {
                'id': str(log.user.id) if log.user else None,
                'email': log.user.email if log.user else None,
                'username': log.user.username if log.user else None,
            } if log.user else None,
            'amount': float(log.amount),
            'currency': log.currency,
            'reference': log.reference,
            'related_entity_type': log.related_entity_type,
            'related_entity_id': str(log.related_entity_id) if log.related_entity_id else None,
            'organization': {
                'id': str(log.organization.id) if log.organization else None,
                'name': log.organization.name if log.organization else None,
            } if log.organization else None,
            'branch': {
                'id': str(log.branch.id) if log.branch else None,
                'name': log.branch.name if log.branch else None,
            } if log.branch else None,
            'notes': log.notes,
            'created_at': log.created_at.isoformat(),
        }
