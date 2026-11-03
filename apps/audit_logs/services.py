"""
Services for the audit_logs application.
"""
from .models import AuditLog, FinancialAuditLog


class AuditLogService:
    """
    Service for audit log operations.
    """
    
    @staticmethod
    def create_audit_log(action, user, entity=None, **kwargs):
        """
        Create an audit log entry.
        """
        log = AuditLog.objects.create(
            action=action,
            user=user,
            user_email=user.email if user else None,
            entity_type=entity.__class__.__name__ if entity else kwargs.get('entity_type'),
            entity_id=entity.id if entity else kwargs.get('entity_id'),
            entity_repr=str(entity)[:255] if entity else kwargs.get('entity_repr'),
            organization=kwargs.get('organization'),
            branch=kwargs.get('branch'),
            ip_address=kwargs.get('ip_address'),
            user_agent=kwargs.get('user_agent'),
            request_path=kwargs.get('request_path'),
            old_values=kwargs.get('old_values', {}),
            new_values=kwargs.get('new_values', {}),
            changed_fields=kwargs.get('changed_fields', []),
            notes=kwargs.get('notes'),
            is_successful=kwargs.get('is_successful', True),
            error_message=kwargs.get('error_message')
        )
        return log
    
    @staticmethod
    def create_financial_audit_log(operation, user, amount, currency='DZD', **kwargs):
        """
        Create a financial audit log entry.
        """
        log = FinancialAuditLog.objects.create(
            operation=operation,
            user=user,
            amount=amount,
            currency=currency,
            reference=kwargs.get('reference'),
            related_entity_type=kwargs.get('related_entity_type'),
            related_entity_id=kwargs.get('related_entity_id'),
            organization=kwargs.get('organization'),
            branch=kwargs.get('branch'),
            notes=kwargs.get('notes')
        )
        return log
