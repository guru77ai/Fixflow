"""
Audit log models.
"""
import uuid
import json
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.core.models import TimeStampedModel, UUIDModel


class AuditLog(UUIDModel, TimeStampedModel):
    """
    Audit log model for tracking changes to business entities.
    """
    # Action types
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('read', 'Read'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('status_change', 'Status Change'),
        ('financial_operation', 'Financial Operation'),
        ('stock_movement', 'Stock Movement'),
        ('document_print', 'Document Print'),
        ('export', 'Export'),
        ('backup', 'Backup'),
        ('restore', 'Restore'),
        ('other', 'Other'),
    ]
    
    action = models.CharField(
        _('Action'),
        max_length=30,
        choices=ACTION_CHOICES,
        db_index=True
    )
    
    # User who performed the action
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name=_('User')
    )
    user_email = models.EmailField(
        _('User Email'),
        blank=True,
        null=True
    )
    
    # Entity information
    entity_type = models.CharField(
        _('Entity Type'),
        max_length=100,
        db_index=True,
        help_text=_('The type of entity (e.g., Repair, Invoice, Payment)')
    )
    entity_id = models.UUIDField(
        _('Entity ID'),
        null=True,
        blank=True,
        db_index=True
    )
    entity_repr = models.CharField(
        _('Entity Representation'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('String representation of the entity')
    )
    
    # Organization and branch context
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name=_('Organization')
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name=_('Branch')
    )
    
    # Request information
    ip_address = models.GenericIPAddressField(
        _('IP Address'),
        blank=True,
        null=True
    )
    user_agent = models.TextField(
        _('User Agent'),
        blank=True,
        null=True
    )
    request_path = models.CharField(
        _('Request Path'),
        max_length=255,
        blank=True,
        null=True
    )
    
    # Change details
    old_values = models.JSONField(
        _('Old Values'),
        default=dict,
        blank=True,
        encoder=json.JSONEncoder
    )
    new_values = models.JSONField(
        _('New Values'),
        default=dict,
        blank=True,
        encoder=json.JSONEncoder
    )
    changed_fields = models.JSONField(
        _('Changed Fields'),
        default=list,
        blank=True,
        help_text=_('List of fields that were changed')
    )
    
    # Additional context
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    # Status
    is_successful = models.BooleanField(
        _('Successful'),
        default=True
    )
    error_message = models.TextField(
        _('Error Message'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['action', 'entity_type']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['organization', 'created_at']),
            models.Index(fields=['branch', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.entity_type} - {self.user}"
    
    @classmethod
    def log_action(cls, action, user, entity=None, **kwargs):
        """
        Helper method to create an audit log entry.
        """
        entity_type = None
        entity_id = None
        entity_repr = None
        
        if entity:
            entity_type = entity.__class__.__name__
            if hasattr(entity, 'id'):
                entity_id = entity.id
            if hasattr(entity, '__str__'):
                entity_repr = str(entity)[:255]
        
        log_entry = cls(
            action=action,
            user=user,
            user_email=user.email if user else None,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_repr=entity_repr,
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
            error_message=kwargs.get('error_message'),
        )
        log_entry.save()
        return log_entry


class FinancialAuditLog(UUIDModel, TimeStampedModel):
    """
    Specialized audit log for financial operations.
    """
    OPERATION_CHOICES = [
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('payment', 'Payment'),
        ('receipt', 'Receipt'),
        ('refund', 'Refund'),
        ('transfer', 'Transfer'),
        ('adjustment', 'Adjustment'),
        ('cancellation', 'Cancellation'),
        ('reversal', 'Reversal'),
    ]
    
    operation = models.CharField(
        _('Operation'),
        max_length=30,
        choices=OPERATION_CHOICES,
        db_index=True
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='financial_audit_logs',
        verbose_name=_('User')
    )
    
    amount = models.DecimalField(
        _('Amount'),
        max_digits=19,
        decimal_places=2,
        default=0
    )
    currency = models.CharField(
        _('Currency'),
        max_length=3,
        default='DZD'
    )
    
    reference = models.CharField(
        _('Reference'),
        max_length=100,
        blank=True,
        null=True
    )
    
    related_entity_type = models.CharField(
        _('Related Entity Type'),
        max_length=100,
        blank=True,
        null=True
    )
    related_entity_id = models.UUIDField(
        _('Related Entity ID'),
        null=True,
        blank=True
    )
    
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='financial_audit_logs',
        verbose_name=_('Organization')
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='financial_audit_logs',
        verbose_name=_('Branch')
    )
    
    notes = models.TextField(
        _('Notes'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Financial Audit Log')
        verbose_name_plural = _('Financial Audit Logs')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['operation', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['organization', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_operation_display()} - {self.amount} {self.currency} - {self.reference}"
